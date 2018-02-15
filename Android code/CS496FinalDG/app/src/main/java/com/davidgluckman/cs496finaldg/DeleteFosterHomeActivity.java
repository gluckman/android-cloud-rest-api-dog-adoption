package com.davidgluckman.cs496finaldg;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.Spinner;

import org.json.JSONArray;
import org.json.JSONException;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.HttpUrl;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

public class DeleteFosterHomeActivity extends AppCompatActivity {

    private OkHttpClient mOkHttpClient;
    private String appDomain = "http://cs496finaldg.appspot.com";
    String selectedId = "";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_delete_foster_home);

        mOkHttpClient = new OkHttpClient();

        // Get JSON list of Foster Homes
        try {
            // Build request URL and query
            HttpUrl reqUrl = HttpUrl.parse(appDomain + "/foster_homes");

            // Build request
            Request request = new Request.Builder()
                    .url(reqUrl)
                    .build();

            // Enqueue request (asynchronous)
            mOkHttpClient.newCall(request).enqueue(new Callback() {
                @Override
                public void onFailure(Call call, IOException e) {
                    e.printStackTrace();
                }

                @Override
                public void onResponse(Call call, Response response) throws IOException {
                    // Store response
                    String r = response.body().string();
                    //Log.i("info", r);
                    try {
                        // Convert response to JSON object
                        JSONArray j = new JSONArray(r);
                        Log.i("json", j.toString());
                        //JSONArray items = j.getJSONArray();
                        // Set up arraylist to store Dogs
                        List homeStrings = new ArrayList<>();
                        final List homeIds = new ArrayList<>();
                        // Store each Dog
                        for(int i = 0; i < j.length(); i++){
                            String homeName = j.getJSONObject(i).getString("name");
                            String option = homeName;
                            String id = j.getJSONObject(i).getString("id");
                            homeStrings.add(option);
                            homeIds.add(id);
                        }
                        // Send Homes to view with adapter
                        final Spinner spinner = (Spinner) findViewById(R.id.deleteHomeSpinner);

                        // Create an ArrayAdapter using the string array and a default spinner layout
                        final ArrayAdapter adapter = new ArrayAdapter<String>(DeleteFosterHomeActivity.this, android.R.layout.simple_spinner_item, homeStrings);
                        // Specify the layout to use when the list of choices appears
                        adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
                        // Apply the adapter to the spinner
                        runOnUiThread(new Runnable() {
                            @Override
                            public void run() {
                                spinner.setAdapter(adapter);
                            }
                        });
                        spinner.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
                            @Override
                            public void onItemSelected(AdapterView<?> adapterView, View view, int position, long l) {

                                selectedId = homeIds.get(position).toString();
                                Log.i("selectedId", selectedId);

                            }

                            @Override
                            public void onNothingSelected(AdapterView<?> parent) {
                                // TODO: Do something here
                            }
                        });
                    } catch (JSONException e2) {
                        e2.printStackTrace();
                    }
                }
            });
        } catch (Exception e) {
            e.printStackTrace();
        }

        ((Button)findViewById(R.id.delete_home_submit_button)).setOnClickListener(new View.OnClickListener() {
            public void onClick (View v){
                try {
                    Request request = new Request.Builder()
                            .url(appDomain + "/foster_homes/" + selectedId)
                            .method("DELETE", RequestBody.create(null, new byte[0]))
                            .build();

                    // Enqueue request (asynchronous)
                    mOkHttpClient.newCall(request).enqueue(new Callback() {
                        @Override
                        public void onFailure(Call call, IOException e) {
                            e.printStackTrace();
                        }

                        @Override
                        public void onResponse(Call call, Response response) throws IOException {
                            // Store response
                            String r = response.body().string();
                            Log.i("info", r);
                        }
                    });

                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
        });
    }
}
