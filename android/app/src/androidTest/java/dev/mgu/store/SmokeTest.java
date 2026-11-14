package dev.mgu.store;
import android.app.*;
import android.os.Bundle;
import com.chaquo.python.*;
import com.chaquo.python.android.AndroidPlatform;

/** Runs on Android, exercising embedded Python and protocol validation without a vehicle. */
public final class SmokeTest extends Instrumentation {
    @Override public void onCreate(Bundle args){super.onCreate(args);start();}
    @Override public void onStart(){Bundle result=new Bundle();try{
        if(!Python.isStarted())Python.start(new AndroidPlatform(getTargetContext()));
        PyObject module=Python.getInstance().getModule("installer");
        if(!module.get("COMMANDS").toString().contains("updater-sources"))throw new AssertionError("Upstream scripts missing");
        PyObject hashlib=Python.getInstance().getModule("hashlib");
        if(hashlib.callAttr("sha256").callAttr("hexdigest").toString().length()!=64)throw new AssertionError("SHA-256 unavailable");
        PhoneApi.Access access=new PhoneApi.Access("http://172.16.222.97:8470/#t=0123456789abcdef0123456789abcdef");
        if(!access.base.equals("http://172.16.222.97:8470"))throw new AssertionError("Base URL");
        try{new PhoneApi.Access("http://example.org/#t=0123456789abcdef0123456789abcdef");throw new AssertionError("Public host accepted");}catch(java.io.IOException expected){}
        if(PhoneApi.privateAddress("192.168.1.999"))throw new AssertionError("Bad IP accepted");
        PyObject release=module.callAttr("download","https://api.github.com/repos/robertnisipeanu/mgu-store/releases/tags/catalog",8*1024*1024,null,"application/vnd.github+json");
        if(!release.toString().contains("catalog.json"))throw new AssertionError("Live catalog metadata unavailable");
        android.graphics.Bitmap icon=android.graphics.Bitmap.createBitmap(512,512,android.graphics.Bitmap.Config.ARGB_8888);
        android.graphics.drawable.Drawable drawable=getTargetContext().getDrawable(R.drawable.ic_mgu_foreground);
        drawable.setBounds(0,0,512,512);drawable.draw(new android.graphics.Canvas(icon));
        try(java.io.FileOutputStream out=getTargetContext().openFileOutput("icon-preview.png",0)){icon.compress(android.graphics.Bitmap.CompressFormat.PNG,100,out);}
        result.putString("stream","PASS: embedded Python import, bundled upstream scripts, SHA-256, phone URL validation and live HTTPS GitHub metadata\n");finish(Activity.RESULT_OK,result);
    }catch(Throwable e){result.putString("stream","FAIL: "+e);finish(Activity.RESULT_CANCELED,result);}}
}
