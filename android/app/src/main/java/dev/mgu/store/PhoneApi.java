package dev.mgu.store;
import org.json.JSONObject;
import java.net.*;
import java.io.*;
import java.nio.charset.StandardCharsets;

final class PhoneApi {
    static final class Access {
        final String base,token;
        Access(String link) throws Exception {
            URI uri=new URI(link.trim());String host=uri.getHost();
            if(!"http".equals(uri.getScheme())||host==null||!privateAddress(host)||uri.getUserInfo()!=null||uri.getQuery()!=null||!(uri.getPath().isEmpty()||uri.getPath().equals("/")))throw new IOException("Use the private IPv4 HTTP link shown by Phone access.");
            String fragment=uri.getRawFragment();
            if(fragment==null||!fragment.matches("t=[a-fA-F0-9]{32,128}"))throw new IOException("The Phone access link needs its #t= token.");
            token=fragment.substring(2);base="http://"+host+":"+(uri.getPort()<0?8470:uri.getPort());
        }
    }
    static boolean privateAddress(String host){
        if(!host.matches("[0-9.]+"))return false;
        String[] parts=host.split("\\.");if(parts.length!=4)return false;int[] n=new int[4];
        try{for(int i=0;i<4;i++){n[i]=Integer.parseInt(parts[i]);if(n[i]>255||n[i]<0)return false;}}catch(Exception e){return false;}
        return n[0]==10||(n[0]==172&&n[1]>=16&&n[1]<=31)||(n[0]==192&&n[1]==168)||(n[0]==169&&n[1]==254);
    }
    static JSONObject request(Access access,android.net.Network network,String path,JSONObject body)throws Exception{
        URL url=new URL(access.base+path);HttpURLConnection c=(HttpURLConnection)(network==null?url.openConnection():network.openConnection(url));
        c.setInstanceFollowRedirects(false);c.setConnectTimeout(10000);c.setReadTimeout(25000);c.setRequestProperty("Authorization","Bearer "+access.token);
        try{
            if(body!=null){c.setRequestMethod("POST");c.setDoOutput(true);c.setRequestProperty("Content-Type","application/json");try(OutputStream out=c.getOutputStream()){out.write(body.toString().getBytes(StandardCharsets.UTF_8));}}
            int code=c.getResponseCode();
            if(code!=200){
                if(code==401)throw new IOException("Phone access token expired. Turn Phone access on again and paste its new link.");
                if(code==429)throw new IOException("Too many attempts. Wait one minute before reconnecting.");
                String detail="";
                try(InputStream in=c.getErrorStream()){
                    if(in!=null){ByteArrayOutputStream error=new ByteArrayOutputStream();byte[] data=new byte[1024];int n;while((n=in.read(data))!=-1&&error.size()<16384)error.write(data,0,Math.min(n,16384-error.size()));detail=new JSONObject(error.toString("UTF-8")).optString("error","");}
                }catch(Exception ignored){}
                throw new IOException("Phone access returned HTTP "+code+(detail.isEmpty()?"":": "+detail));
            }
            ByteArrayOutputStream bytes=new ByteArrayOutputStream();try(InputStream in=c.getInputStream()){byte[] b=new byte[8192];int n;while((n=in.read(b))!=-1){if(bytes.size()+n>8*1024*1024)throw new IOException("Response too large");bytes.write(b,0,n);}}
            JSONObject reply=new JSONObject(bytes.toString("UTF-8"));if(reply.has("error")&&!reply.isNull("error"))throw new IOException(reply.optString("error"));return reply;
        }finally{c.disconnect();}
    }
}
