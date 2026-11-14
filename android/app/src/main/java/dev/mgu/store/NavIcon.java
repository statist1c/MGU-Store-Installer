package dev.mgu.store;
import android.content.Context;
import android.graphics.*;
import android.view.View;

/** Small native line icons, matching the Root Companion navigation style. */
final class NavIcon extends View {
    int color;final int kind;final Paint p=new Paint(Paint.ANTI_ALIAS_FLAG);
    NavIcon(Context context,int value){super(context);kind=value;setImportantForAccessibility(IMPORTANT_FOR_ACCESSIBILITY_NO);}
    @Override protected void onDraw(Canvas canvas){super.onDraw(canvas);canvas.save();canvas.scale(getWidth()/24f,getHeight()/24f);p.setColor(color);p.setStyle(Paint.Style.STROKE);p.setStrokeWidth(1.8f);p.setStrokeCap(Paint.Cap.ROUND);p.setStrokeJoin(Paint.Join.ROUND);
        if(kind==0){canvas.drawLine(12,3,12,15,p);canvas.drawLine(7,10,12,15,p);canvas.drawLine(17,10,12,15,p);canvas.drawLine(4,17,4,21,p);canvas.drawLine(4,21,20,21,p);canvas.drawLine(20,21,20,17,p);}
        if(kind==1){canvas.drawRoundRect(3,4,21,21,2,2,p);canvas.drawLine(3,9,21,9,p);canvas.drawLine(8,3,8,6,p);canvas.drawLine(16,3,16,6,p);canvas.drawLine(8,13,10,13,p);canvas.drawLine(14,13,16,13,p);canvas.drawLine(8,17,10,17,p);canvas.drawLine(14,17,16,17,p);}
        if(kind==2){canvas.drawRoundRect(2,4,22,20,2,2,p);Path path=new Path();path.moveTo(4,13);path.lineTo(8,13);path.lineTo(10,8);path.lineTo(14,17);path.lineTo(16,12);path.lineTo(20,12);canvas.drawPath(path,p);}
        if(kind==3){canvas.drawCircle(12,12,6,p);canvas.drawCircle(12,12,2,p);for(int i=0;i<8;i++){double a=i*Math.PI/4;canvas.drawLine(12+(float)Math.cos(a)*7,12+(float)Math.sin(a)*7,12+(float)Math.cos(a)*9,12+(float)Math.sin(a)*9,p);}}
        canvas.restore();
    }
}
