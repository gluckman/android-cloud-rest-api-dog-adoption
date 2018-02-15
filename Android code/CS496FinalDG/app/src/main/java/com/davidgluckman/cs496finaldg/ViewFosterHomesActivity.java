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

public class ViewFosterHomesActivity extends AppCompatActivity {

    //private ListView lv;

    // Create necessary objects
    private OkHttpClient mOkHttpClient;
    private String appDomain = "http://cs496finaldg.appspot.com";

    // Create JSON media type
    public static final MediaType JSON = MediaType.parse("application/json");

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_view_foster_homes);
        //lv = (ListView) findViewById(R.id.dog_list);

        mOkHttpClient = new OkHttpClient();

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
                        // Set up map to store Foster Homes
                        List<Map<String,String>> homes = new ArrayList<Map<String,String>>();
                        // Store each Home
                        for(int i = 0; i < j.length(); i++){
                            HashMap<String, String> m = new HashMap<String, String>();
                            m.put("name", j.getJSONObject(i).getString("name"));

                            String homeAddress = j.getJSONObject(i).getString("address");
                            if (homeAddress.equals("null")) {
                                homeAddress = "-";
                            }
                            m.put("address", homeAddress);

                            String homePhone = j.getJSONObject(i).getString("phone");
                            if (homePhone.equals("null")) {
                                homePhone = "-";
                            }
                            m.put("phone",homePhone);

                            String homeChildren = j.getJSONObject(i).getString("has_children");
                            if (homeChildren.equals("true")) {
                                homeChildren = "Yes";
                            }
                            else
                                homeChildren = "No";
                            m.put("has_children",homeChildren);

                            String homePets = j.getJSONObject(i).getString("has_other_pets");
                            if (homePets.equals("true")) {
                                homePets = "Yes";
                            }
                            else
                                homePets = "No";
                            m.put("has_other_pets",homePets);
                            homes.add(m);
                        }
                        // Send Foster Homes to view with adapter
                        final SimpleAdapter homeAdapter = new SimpleAdapter(
                                getApplicationContext(),
                                homes,
                                R.layout.home_list_layout,
                                new String[] {"name", "address", "phone", "has_children", "has_other_pets"},
                                new int[] {R.id.homeName, R.id.homeAddress, R.id.homePhone, R.id.homeChildren, R.id.homePets});
                        runOnUiThread(new Runnable() {
                            @Override
                            public void run() {
                                ((ListView)findViewById(R.id.home_list)).setAdapter(homeAdapter);
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
