package com.davidgluckman.cs496finaldg;

import android.content.Intent;
import android.support.annotation.Nullable;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
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
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

public class MainActivity extends AppCompatActivity {

    // Create necessary objects
    private OkHttpClient mOkHttpClient;
    private String appDomain = "http://cs496finaldg.appspot.com";

    // Create JSON media type
    public static final MediaType JSON = MediaType.parse("application/json");

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        mOkHttpClient = new OkHttpClient();

        // View Dogs button setup
        ((Button) findViewById(R.id.view_dogs_button)).setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                Intent intent = new Intent(MainActivity.this, ViewDogsActivity.class);
                startActivity(intent);
            }
        });

        // Add Dog button setup
        ((Button) findViewById(R.id.add_dog_button)).setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                Intent intent = new Intent(MainActivity.this, AddDogActivity.class);
                startActivity(intent);
            }
        });

        // Modify Dog button setup
        ((Button) findViewById(R.id.modify_dog_button)).setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                Intent intent = new Intent(MainActivity.this, ModifyDogActivity.class);
                startActivity(intent);
            }
        });

        // Delete Dog button setup
        ((Button) findViewById(R.id.delete_dog_button)).setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                Intent intent = new Intent(MainActivity.this, DeleteDogActivity.class);
                startActivity(intent);
            }
        });

        // Adopt Dog button setup
        ((Button) findViewById(R.id.adopt_dog_button)).setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                Intent intent = new Intent(MainActivity.this, AdoptDogActivity.class);
                startActivity(intent);
            }
        });

        // View Foster Homes button setup
        ((Button) findViewById(R.id.view_foster_homes_button)).setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                Intent intent = new Intent(MainActivity.this, ViewFosterHomesActivity.class);
                startActivity(intent);
            }
        });

        // Add Foster Home button setup
        ((Button) findViewById(R.id.add_foster_home_button)).setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                Intent intent = new Intent(MainActivity.this, AddFosterHomeActivity.class);
                startActivity(intent);
            }
        });

        // Modify Foster Home button setup
        ((Button) findViewById(R.id.modify_foster_home_button)).setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                Intent intent = new Intent(MainActivity.this, ModifyFosterHomeActivity.class);
                startActivity(intent);
            }
        });

        // Delete Foster Home button setup
        ((Button) findViewById(R.id.delete_foster_home_button)).setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                Intent intent = new Intent(MainActivity.this, DeleteFosterHomeActivity.class);
                startActivity(intent);
            }
        });

        // Place Foster Dog button setup
        ((Button) findViewById(R.id.foster_dog_button)).setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                Intent intent = new Intent(MainActivity.this, PlaceFosterDogActivity.class);
                startActivity(intent);
            }
        });

        // Remove Foster Dog button setup
        ((Button) findViewById(R.id.unfoster_dog_button)).setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                Intent intent = new Intent(MainActivity.this, RemoveFosterDogActivity.class);
                startActivity(intent);
            }
        });
    }
}
