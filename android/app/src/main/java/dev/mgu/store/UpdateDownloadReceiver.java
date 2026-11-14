package dev.mgu.store;

import android.app.DownloadManager;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;

/** Only the app's tracked DownloadManager request can trigger APK validation. */
public final class UpdateDownloadReceiver extends BroadcastReceiver {
    @Override public void onReceive(Context context, Intent intent) {
        if (!DownloadManager.ACTION_DOWNLOAD_COMPLETE.equals(intent.getAction())) return;
        long id = intent.getLongExtra(DownloadManager.EXTRA_DOWNLOAD_ID, -1);
        if (id < 0 || id != AppUpdater.prefs(context).getLong("download_id", -2)) return;
        // Hashing is done by a scheduled job, outside the receiver's short execution window.
        AppUpdater.scheduleValidation(context);
    }
}
