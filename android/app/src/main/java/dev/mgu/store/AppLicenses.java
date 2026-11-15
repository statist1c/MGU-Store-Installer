// SPDX-License-Identifier: GPL-3.0-or-later
package dev.mgu.store;

import android.app.Activity;
import android.app.AlertDialog;
import android.graphics.Typeface;
import android.widget.ScrollView;
import android.widget.TextView;
import java.io.ByteArrayOutputStream;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.Arrays;

/** Displays the exact notice texts packaged from the repository by Gradle. */
final class AppLicenses {
    static void show(Activity activity) {
        try {
            ArrayList<String> names = new ArrayList<>(Arrays.asList("LICENSE", "COPYRIGHT.md", "THIRD_PARTY_NOTICES.md", "SOURCE.md"));
            String[] files = activity.getAssets().list("legal/LICENSES");
            if (files != null) {
                Arrays.sort(files);
                for (String file : files) if (!file.equals("PROVENANCE.json")) names.add("LICENSES/" + file);
            }
            new AlertDialog.Builder(activity).setTitle("Open-source licenses")
                    .setItems(names.toArray(new String[0]), (dialog, index) -> display(activity, names.get(index)))
                    .setNegativeButton("Close", null).show();
        } catch (Exception error) {
            new AlertDialog.Builder(activity).setTitle("Licenses unavailable").setMessage(error.getMessage()).setPositiveButton("OK", null).show();
        }
    }
    private static void display(Activity activity, String name) {
        try (InputStream in = activity.getAssets().open("legal/" + name); ByteArrayOutputStream out = new ByteArrayOutputStream()) {
            byte[] buffer = new byte[8192]; int count;
            while ((count = in.read(buffer)) != -1) out.write(buffer, 0, count);
            TextView text = new TextView(activity);
            text.setText(new String(out.toByteArray(), StandardCharsets.UTF_8));
            text.setTextSize(12); text.setTypeface(Typeface.MONOSPACE); text.setTextIsSelectable(true);
            int padding = Math.round(16 * activity.getResources().getDisplayMetrics().density);
            text.setPadding(padding, padding, padding, padding);
            ScrollView scroll = new ScrollView(activity); scroll.addView(text);
            new AlertDialog.Builder(activity).setTitle(name).setView(scroll).setPositiveButton("Close", null).show();
        } catch (Exception error) {
            new AlertDialog.Builder(activity).setTitle("License unavailable").setMessage(error.getMessage()).setPositiveButton("OK", null).show();
        }
    }
}
