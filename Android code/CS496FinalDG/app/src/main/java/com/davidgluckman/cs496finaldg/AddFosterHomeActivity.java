package com.davidgluckman.cs496finaldg;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.RadioButton;
import android.widget.RadioGroup;

import org.json.JSONObject;

import java.io.IOException;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.MediaType;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

public class AddFosterHomeActivity extends AppCompatActivity {

    private OkHttpClient mOkHttpClient;
    private String appDomain = "http://cs496finaldg.appspot.com";

    // Create JSON media type
    public static final MediaType JSON = MediaType.parse("application/json");

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_add_foster_home);

        mOkHttpClient = new OkHttpClient();

        ((Button)findViewById(R.id.submit_home_button)).setOnClickListener(new View.OnClickListener() {
            public void onClick (View v){
                try {
                    // Organize JSON
                    JSONObject json = new JSONObject();
                    // Add name
                    json.put("name", ((EditText) findViewById(R.id.newHomeName)).getText().toString());
                    // Check for address
                    if (!((EditText) findViewById(R.id.newHomeAddress)).getText().toString().matches("")) {
                        // Add breed
                        json.put("address", ((EditText) findViewById(R.id.newHomeAddress)).getText().toString());
                    }
                    // Check for phone
                    if (!((EditText) findViewById(R.id.newHomePhone)).getText().toString().matches("")) {
                        // Add phone
                        json.put("phone", ((EditText) findViewById(R.id.newHomePhone)).getText().toString());
                    }

                    RadioGroup rg1 = (RadioGroup)findViewById(R.id.childrenButtons);
                    String newHomeChildren;
                    if(rg1.getCheckedRadioButtonId() != -1) {
                        int id = rg1.getCheckedRadioButtonId();
                        View radioButton = rg1.findViewById(id);
                        int radioId = rg1.indexOfChild(radioButton);
                        RadioButton btn = (RadioButton) rg1.getChildAt(radioId);
                        String selection = (String) btn.getText();
                        if (selection.equals("No"))
                            json.put("has_children", false);
                        else
                            json.put("has_children", true);
                    }

                    RadioGroup rg2 = (RadioGroup)findViewById(R.id.petsButtons);
                    String newHomePets;
                    if(rg2.getCheckedRadioButtonId() != -1) {
                        int id = rg2.getCheckedRadioButtonId();
                        View radioButton = rg2.findViewById(id);
                        int radioId = rg2.indexOfChild(radioButton);
                        RadioButton btn = (RadioButton) rg2.getChildAt(radioId);
                        String selection = (String) btn.getText();
                        if (selection.equals("No"))
                            json.put("has_other_pets", false);
                        else
                            json.put("has_other_pets", true);
                    }

                    String message = json.toString();
                    // Build request
                    RequestBody body = RequestBody.create(JSON, message);

                    Request request = new Request.Builder()
                            .url(appDomain + "/foster_homes")
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
