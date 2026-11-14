package dev.mgu.store;

import android.app.job.JobParameters;
import android.app.job.JobService;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;

public final class UpdateValidationJob extends JobService {
    private final ExecutorService worker = Executors.newSingleThreadExecutor();
    private Future<?> task;
    @Override public boolean onStartJob(JobParameters params) {
        task = worker.submit(() -> {
            try { AppUpdater.validateDownload(this); }
            catch (Exception error) { AppUpdater.rejectDownload(this, error.getMessage()); }
            finally { jobFinished(params, false); }
        });
        return true;
    }
    @Override public boolean onStopJob(JobParameters params) { if (task != null) task.cancel(true); return true; }
    @Override public void onDestroy() { worker.shutdownNow(); super.onDestroy(); }
}
