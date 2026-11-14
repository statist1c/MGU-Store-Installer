package dev.mgu.store;

import android.app.*;
import android.content.*;
import android.os.*;
import com.chaquo.python.*;
import com.chaquo.python.android.AndroidPlatform;
import org.json.JSONObject;
import java.io.*;
import java.util.concurrent.*;

public final class InstallService extends Service {
    public static volatile boolean busy;
    public static volatile String status="Ready · connect to your head unit", pendingFingerprint="",pendingHost="";
    private static String output="";
    private final ExecutorService worker=Executors.newSingleThreadExecutor();
    public synchronized void onLine(String line){synchronized(InstallService.class){output+=line+"\n";if(output.length()>500000)output=output.substring(output.length()-500000);} }
    public static synchronized String log(){return output;}
    public static synchronized void clear(){if(!busy)output="";}
    @Override public IBinder onBind(Intent i){return null;}
    @Override public int onStartCommand(Intent intent,int flags,int startId){
        if(intent==null){stopSelf();return START_NOT_STICKY;}
        if(busy)return START_NOT_STICKY;
        busy=true;pendingFingerprint="";pendingHost="";status="Connecting over SSH…";
        NotificationManager manager=getSystemService(NotificationManager.class);
        manager.createNotificationChannel(new NotificationChannel("install","Store installation",NotificationManager.IMPORTANCE_LOW));
        PendingIntent open=PendingIntent.getActivity(this,0,new Intent(this,MainActivity.class),PendingIntent.FLAG_IMMUTABLE|PendingIntent.FLAG_UPDATE_CURRENT);
        Notification n=new Notification.Builder(this,"install").setSmallIcon(dev.mgu.store.R.drawable.ic_status).setContentTitle("MGU Store Installer").setContentText("Head-unit operation in progress").setContentIntent(open).setOngoing(true).build();
        startForeground(1,n);
        PowerManager.WakeLock lock=((PowerManager)getSystemService(POWER_SERVICE)).newWakeLock(PowerManager.PARTIAL_WAKE_LOCK,"mgu:install");lock.acquire(75*60*1000L);
        worker.execute(()->{
            String action=intent.getStringExtra("action");
            try(SshClient ssh=new SshClient(this,intent.getStringExtra("host"),intent.getIntExtra("port",22),intent.getStringExtra("pass"),intent.getStringExtra("route"),intent.getBooleanExtra("legacy",false))){
                intent.removeExtra("pass");
                status="SSH authenticated · "+action;onLine(status);
                if(!Python.isStarted())Python.start(new AndroidPlatform(this));
                PyObject backend=Python.getInstance().getModule("installer");
                if("install".equals(action)){
                    backend.callAttr("install",new File(getCacheDir(),"kit").getPath(),ssh,this,intent.getBooleanExtra("renderer",true),intent.getBooleanExtra("uplink",true));
                    status="Install command completed · review the log";
                }else if("restart".equals(action)){
                    backend.callAttr("restart",ssh);status="Restart requested · reconnect after boot";
                }else{
                    JSONObject reply=new JSONObject(ssh.run("sh /var/opt/mgu-deploy/mgu-deploy.sh status", "",180));
                    if(reply.getInt("rc")!=0)throw new IOException("Deploy status failed. The Store may not be installed; inspect the log.");
                    status="SSH authenticated · status received";
                }
            }catch(Exception e){onLine("ERROR: "+e.getMessage());status=pendingFingerprint.isEmpty()?"Operation failed · see Monitor":"SSH identity requires verification · see Setup";}
            finally{busy=false;if(lock.isHeld())lock.release();stopForeground(STOP_FOREGROUND_REMOVE);stopSelf(startId);}
        });
        return START_NOT_STICKY;
    }
}
