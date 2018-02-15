package com.davidgluckman.cs496finaldg;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.widget.ListView;
import android.widget.SimpleAdapter;

import org.json.JSONArray;
import org.json.JSONException;

import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.HttpUrl;
import okhttp3.MediaType;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;

public class ViewDogsActivity extends AppCompatActivity {

    //private ListView lv;

    // Create necessary objects
    private OkHttpClient mOkHttpClient;
    private String appDomain = "http://cs496finaldg.appspot.com";

    // Create JSON media type
    public static final MediaType JSON = MediaType.parse("application/json");

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_view_dogs);

        mOkHttpClient = new OkHttpClient();

        try {
            // Build request URL and query
            HttpUrl reqUrl = HttpUrl.parse(appDomain + "/dogs");

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
                        // Set up map to store Dogs
                        List<Map<String,String>> dogs = new ArrayList<Map<String,String>>();
                        // Store each Dog
                        for(int i = 0; i < j.length(); i++){
                            HashMap<String, String> m = new HashMap<String, String>();
                            m.put("name", j.getJSONObject(i).getString("name"));

                            String dogBreed = j.getJSONObject(i).getString("breed");
                            if (dogBreed.equals("null")) {
                                dogBreed = "-";
                            }
                            m.put("breed", dogBreed);

                            String dogBirthdate = j.getJSONObject(i).getString("birthdate");
                            if (dogBirthdate.equals("null")) {
                                dogBirthdate = "-";
                            }
                            m.put("birthdate",dogBirthdate);
                            String dogAdopted = j.getJSONObject(i).getString("adopted");
                            if (dogAdopted.equals("true")) {
                                dogAdopted = "Yes";
                            }
                            else
                                dogAdopted = "No";
                            m.put("adopted",dogAdopted);

                            String dogFostered = j.getJSONObject(i).getString("fostered");
                            if (dogFostered.equals("true")) {
                                dogFostered = "Yes";
                            }
                            else
                                dogFostered = "No";
                            m.put("fostered",dogFostered);
                            dogs.add(m);
                        }
                        // Send Dogs to view with adapter
                        final SimpleAdapter dogAdapter = new SimpleAdapter(
                                getApplicationContext(),
                                dogs,
                                R.layout.dog_list_layout,
                                new String[] {"name", "breed", "birthdate", "adopted", "fostered"},
                                new int[] {R.id.dogName, R.id.dogBreed, R.id.dogBirthdate, R.id.dogAdopted, R.id.dogFostered});
//                                        ((ListView)findViewById(R.id.dog_list)).setAdapter(dogAdapter);
                        runOnUiThread(new Runnable() {
                            @Override
                            public void run() {
                                ((ListView)findViewById(R.id.dog_list)).setAdapter(dogAdapter);
                            }
                        });
                    } catch (JSONException e2) {
                        e2.printStackTrace();
                    }
                }
            });
//                        }
//                    });
        } catch (Exception e) {
            e.printStackTrace();
        }

    }

}
