package dev.mgu.store;

import android.content.*;
import android.net.*;
import android.util.Base64;
import com.jcraft.jsch.*;
import org.bouncycastle.jce.provider.BouncyCastleProvider;
import org.json.JSONObject;
import java.io.*;
import java.net.Socket;
import java.nio.charset.StandardCharsets;
import java.security.*;

/** One authenticated SSH session per explicit operation. Host keys never auto-rotate. */
public final class SshClient implements AutoCloseable {
    private Session session;
    private final InstallService service;
    public SshClient(InstallService context, String host, int port, String passphrase, String route, boolean legacy) throws Exception {
        service=context;
        Security.removeProvider("BC"); Security.addProvider(new BouncyCastleProvider());
        JSch ssh=new JSch();
        ssh.setHostKeyRepository(new HostKeyRepository(){
            public int check(String address,byte[] key){
                try {
                    String fp="SHA256:"+Base64.encodeToString(MessageDigest.getInstance("SHA-256").digest(key),Base64.NO_WRAP|Base64.NO_PADDING);
                    String saved=context.getSharedPreferences("pins",0).getString(host+":"+port,"");
                    if(!fp.equals(saved)) { service.pendingFingerprint=fp; service.pendingHost=host+":"+port; service.onLine((saved.isEmpty()?"Verify first-use SSH identity: ":"HOST KEY CHANGED. Connection refused: ")+fp); return saved.isEmpty()?NOT_INCLUDED:CHANGED; }
                    return OK;
                }catch(Exception e){return CHANGED;}
            }
            public void add(HostKey k,UserInfo u){} public void remove(String h,String t){} public void remove(String h,String t,byte[] k){}
            public String getKnownHostsRepositoryID(){return "MGU verified host fingerprints";}
            public HostKey[] getHostKey(){return new HostKey[0];} public HostKey[] getHostKey(String h,String t){return new HostKey[0];}
        });
        File key=new File(context.getFilesDir(),"root-key");
        if(!key.isFile()) throw new IOException("Import root's SSH private key first.");
        ssh.addIdentity(key.getPath(),passphrase.isEmpty()?null:passphrase);
        session=ssh.getSession("root",host,port);
        session.setConfig("StrictHostKeyChecking","yes"); session.setConfig("PreferredAuthentications","publickey");
        if(legacy){ session.setConfig("server_host_key",JSch.getConfig("server_host_key")+",ssh-rsa"); session.setConfig("PubkeyAcceptedAlgorithms",JSch.getConfig("PubkeyAcceptedAlgorithms")+",ssh-rsa"); }
        ConnectivityManager manager=(ConnectivityManager)context.getSystemService(Context.CONNECTIVITY_SERVICE);
        final Network network;
        if(!route.equals("Automatic")){
            Network found=null;
            for(Network n:manager.getAllNetworks()){
                NetworkCapabilities caps=manager.getNetworkCapabilities(n);
                if(caps!=null && caps.hasTransport(route.equals("Wi-Fi")?NetworkCapabilities.TRANSPORT_WIFI:NetworkCapabilities.TRANSPORT_ETHERNET)) {found=n;break;}
            }
            if(found==null)throw new IOException("Selected "+route+" network is unavailable.");
            network=found;
        }else network=null;
        session.setSocketFactory(new com.jcraft.jsch.SocketFactory(){
            public Socket createSocket(String h,int p)throws IOException {Socket s=network==null?new Socket():network.getSocketFactory().createSocket();s.connect(new java.net.InetSocketAddress(h,p),15000);s.setSoTimeout(30000);return s;}
            public InputStream getInputStream(Socket s)throws IOException{return s.getInputStream();}
            public OutputStream getOutputStream(Socket s)throws IOException{return s.getOutputStream();}
        });
        session.setServerAliveInterval(10000);session.setServerAliveCountMax(6);
        try{session.connect(20000);}catch(Exception e){session.disconnect();throw e;}
    }
    private final class Capture extends OutputStream {
        final ByteArrayOutputStream data=new ByteArrayOutputStream();
        final boolean logging;
        Capture(boolean logs){logging=logs;}
        public synchronized void write(int b){if(data.size()<2*1024*1024)data.write(b);}
        public synchronized void write(byte[] b,int off,int len){int n=Math.min(len,2*1024*1024-data.size());if(n>0)data.write(b,off,n);if(logging)service.onLine(new String(b,off,len,StandardCharsets.UTF_8));}
        synchronized String text(){return new String(data.toByteArray(),StandardCharsets.UTF_8);}
    }
    public String run(String command,String inputPath,int timeout) {
        ChannelExec channel=null;InputStream input=null;Capture out=new Capture(true),err=new Capture(true);
        try{
            if(timeout<1||timeout>3600)throw new IOException("Invalid timeout");
            if(!inputPath.isEmpty()){
                File f=new File(inputPath).getCanonicalFile();
                if(!f.getPath().startsWith(service.getCacheDir().getCanonicalPath()+File.separator))throw new IOException("Invalid input file");
                input=new FileInputStream(f);
            }else input=new ByteArrayInputStream(new byte[0]);
            channel=(ChannelExec)session.openChannel("exec");channel.setCommand(command);channel.setInputStream(input);channel.setOutputStream(out);channel.setErrStream(err);channel.connect(20000);
            long deadline=android.os.SystemClock.elapsedRealtime()+timeout*1000L;
            while(!channel.isClosed()) {if(android.os.SystemClock.elapsedRealtime()>deadline)throw new IOException("SSH operation timed out. Remote work may still be running; inspect status before retrying.");Thread.sleep(100);}
            return new JSONObject().put("rc",channel.getExitStatus()).put("out",out.text()).put("err",err.text()).toString();
        }catch(Exception e){try{return new JSONObject().put("rc",255).put("out",out.text()).put("err",err.text()+"\n"+e.getMessage()).toString();}catch(Exception impossible){return "{}";}}
        finally{if(channel!=null)channel.disconnect();try{if(input!=null)input.close();}catch(IOException ignored){}}
    }
    public void close(){if(session!=null)session.disconnect();}
}
