package com.davidgluckman.cs496finaldg;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ListView;
import android.widget.SimpleAdapter;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.HttpUrl;
import okhttp3.MediaType;
import okhttp3.MultipartBody;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

public class AddDogActivity extends AppCompatActivity {

    private OkHttpClient mOkHttpClient;
    private String appDomain = "http://cs496finaldg.appspot.com";

    // Create JSON media type
    public static final MediaType JSON = MediaType.parse("application/json");

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_add_dog);

        mOkHttpClient = new OkHttpClient();

        ((Button)findViewById(R.id.submit_dog_button)).setOnClickListener(new View.OnClickListener() {
            public void onClick (View v){
                try {
                    // Organize JSON
                    JSONObject json = new JSONObject();
                    // Add name
                    json.put("name", ((EditText) findViewById(R.id.newDogName)).getText().toString());
                    // Check for breed
                    if (!((EditText) findViewById(R.id.newDogBreed)).getText().toString().matches("")) {
                        // Add breed
                        json.put("breed", ((EditText) findViewById(R.id.newDogBreed)).getText().toString());
                    }
                    // Check for birthdate
                    if (!((EditText) findViewById(R.id.newDogBirthdate)).getText().toString().matches("")) {
                        // Add birthdate
                        json.put("birthdate", ((EditText) findViewById(R.id.newDogBirthdate)).getText().toString());
                    }

                    String message = json.toString();
                    // Build request
                    RequestBody body = RequestBody.create(JSON, message);

                    Request request = new Request.Builder()
                            .url(appDomain + "/dogs")
                            .method("POST", RequestBody.create(null, new byte[0]))
                            .post(body)
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

