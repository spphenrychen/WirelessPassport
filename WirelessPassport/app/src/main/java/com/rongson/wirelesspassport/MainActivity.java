package com.rongson.wirelesspassport;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.net.wifi.p2p.WifiP2pDevice;
import android.net.wifi.p2p.WifiP2pDeviceList;
import android.net.wifi.p2p.WifiP2pManager;
import android.net.wifi.p2p.nsd.WifiP2pServiceInfo;
import android.net.wifi.p2p.nsd.WifiP2pServiceRequest;
import android.support.v7.app.AlertDialog;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.ListView;
import android.widget.TextView;

import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.Collection;
import java.util.List;

public class MainActivity extends AppCompatActivity {
    String TAG = "Wireless Passport MainActivity";
    WifiP2pManager mManager;
    WifiP2pManager.Channel mChannel;
    BroadcastReceiver mReceiver;
    IntentFilter mIntentFilter;
    WifiP2pServiceRequest req;
    Button sendBroadcast;
    TextView serverStatusText;



    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        //sendBroadcast = (Button) findViewById(R.id.button);
        //sendBroadcast.setOnClickListener(sendListener);

        serverStatusText = (TextView) findViewById(R.id.ServerStatusText);


        mManager = (WifiP2pManager) getSystemService(Context.WIFI_P2P_SERVICE);
        mChannel = mManager.initialize(this, getMainLooper(), null);
        mReceiver = new WiFiDirectBroadcastReceiver(mManager, mChannel, this);
        mIntentFilter = new IntentFilter();
        mIntentFilter.addAction(WifiP2pManager.WIFI_P2P_STATE_CHANGED_ACTION);
        mIntentFilter.addAction(WifiP2pManager.WIFI_P2P_PEERS_CHANGED_ACTION);
        mIntentFilter.addAction(WifiP2pManager.WIFI_P2P_CONNECTION_CHANGED_ACTION);
        mIntentFilter.addAction(WifiP2pManager.WIFI_P2P_THIS_DEVICE_CHANGED_ACTION);

        // 在接收端那邊可以找到這個名字，也可以用device.getaddress之類的api找到該wireless passport的mac address
        setDeviceName("WirelessPassportDevice");

        mManager.discoverPeers(mChannel, new WifiP2pManager.ActionListener() {
            @Override
            public void onSuccess() {
                //...

                Log.e(TAG,"discoverPeers onSuccess");
            }

            @Override
            public void onFailure(int reasonCode) {
                //...
                Log.e(TAG,"discoverPeers onFailure");
            }
        });

        Log.e(TAG,"in onCreate");

    }



    private Button.OnClickListener sendListener = new Button.OnClickListener(){
        @Override
        public void onClick(View v1){
            //get myself device name
            //WifiP2pDevice device = intent.getParcelableExtra(WifiP2pManager.EXTRA_WIFI_P2P_DEVICE);
            //String thisDeviceName = device.deviceName;
            //Log.e(TAG+" state changed","devicename: "+thisDeviceName);
            //displayPeers();

        }
    };


    /* register the broadcast receiver with the intent values to be matched */
    @Override
    protected void onResume() {
        super.onResume();
        registerReceiver(mReceiver, mIntentFilter);
        serverStatusText.setText("RegisterReceiver");
        Log.e(TAG,"in onResume");
    }
    /* unregister the broadcast receiver */
    @Override
    protected void onPause() {
        super.onPause();
        unregisterReceiver(mReceiver);
        serverStatusText.setText("UnregisterReceiver");
        Log.e(TAG,"in onPause");
    }

    public void setDeviceName(String devName) {
        try {
            Class[] paramTypes = new Class[3];
            paramTypes[0] = WifiP2pManager.Channel.class;
            paramTypes[1] = String.class;
            paramTypes[2] = WifiP2pManager.ActionListener.class;
            Method setDeviceName = mManager.getClass().getMethod(
                    "setDeviceName", paramTypes);
            setDeviceName.setAccessible(true);

            Object arglist[] = new Object[3];
            arglist[0] = mChannel;
            arglist[1] = devName;
            arglist[2] = new WifiP2pManager.ActionListener() {

                @Override
                public void onSuccess() {
                    Log.i("setDeviceName,onSuccess","setDeviceName succeeded");
                }

                @Override
                public void onFailure(int reason) {
                    Log.i("setDeviceName,onSuccess","setDeviceName failed");
                }
            };

            setDeviceName.invoke(mManager, arglist);

        } catch (NoSuchMethodException e) {
            e.printStackTrace();
        } catch (IllegalAccessException e) {
            e.printStackTrace();
        } catch (IllegalArgumentException e) {
            e.printStackTrace();
        } catch (InvocationTargetException e) {
            e.printStackTrace();
        }
    }

    public void displayPeers(final WifiP2pDeviceList peers)
    {
        //Dialog to show errors/status
        final AlertDialog.Builder dialog = new AlertDialog.Builder(this);
        dialog.setTitle("WiFi Direct display peers");

        //Get list view
        ListView peerView = (ListView) findViewById(R.id.peers_listview);

        //Make array list
        ArrayList<String> peersStringArrayList = new ArrayList<String>();

        //Fill array list with strings of peer names
        for(WifiP2pDevice wd : peers.getDeviceList())
        {
            peersStringArrayList.add(wd.deviceName);
        }

        //Set list view as clickable
        peerView.setClickable(true);

        //Make adapter to connect peer data to list view
        ArrayAdapter arrayAdapter = new ArrayAdapter(this, android.R.layout.simple_list_item_1, peersStringArrayList.toArray());

        //Show peer data in listview
        peerView.setAdapter(arrayAdapter);


        peerView.setOnItemClickListener(new AdapterView.OnItemClickListener() {

            public void onItemClick(AdapterView<?> arg0, View view, int arg2,long arg3) {

                //Get string from textview
                TextView tv = (TextView) view;

                WifiP2pDevice device = null;

                //Search all known peers for matching name
                for(WifiP2pDevice wd : peers.getDeviceList())
                {
                    if(wd.deviceName.equals(tv.getText()))
                        device = wd;
                }

                if(device != null)
                {
                    //Connect to selected peer
                    //connectToPeer(device);
                    Log.e(TAG, "want to connect to device");

                }
                else
                {
                    dialog.setMessage("Failed");
                    dialog.show();

                }
            }
            // TODO Auto-generated method stub
        });

    }

}
