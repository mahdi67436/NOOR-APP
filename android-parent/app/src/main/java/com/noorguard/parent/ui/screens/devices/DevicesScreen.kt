package com.noorguard.parent.ui.screens.devices

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.ViewModel
import dagger.hilt.android.lifecycle.HiltViewModel
import javax.inject.Inject
import com.noorguard.parent.ui.theme.*

@HiltViewModel
class DevicesViewModel @Inject constructor() : ViewModel() {
    var devices = listOf(
        DeviceInfo("1", "Samsung Galaxy S21", "android", true, true),
        DeviceInfo("2", "Samsung Galaxy Tab S8", "android", true, false),
        DeviceInfo("3", "iPhone 14", "ios", false, true)
    )
}

data class DeviceInfo(
    val id: String,
    val name: String,
    val type: String,
    val isOnline: Boolean,
    val isTrusted: Boolean
)

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun DevicesScreen(
    onNavigateBack: () -> Unit,
    viewModel: DevicesViewModel = hiltViewModel()
) {
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Devices", fontWeight = FontWeight.Bold) },
                navigationIcon = {
                    IconButton(onClick = onNavigateBack) {
                        Icon(Icons.Default.ArrowBack, contentDescription = "Back")
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = EmeraldGreen,
                    titleContentColor = Color.White,
                    navigationIconContentColor = Color.White
                )
            )
        },
        floatingActionButton = {
            FloatingActionButton(
                onClick = { /* Add device */ },
                containerColor = EmeraldGreen
            ) {
                Icon(Icons.Default.Add, contentDescription = "Add Device")
            }
        }
    ) { paddingValues ->
        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
                .padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            items(viewModel.devices) { device ->
                DeviceCard(device = device)
            }
        }
    }
}

@Composable
fun DeviceCard(device: DeviceInfo) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Icon(
                imageVector = if (device.type == "android") Icons.Default.PhoneAndroid 
                              else Icons.Default.PhoneIphone,
                contentDescription = null,
                modifier = Modifier.size(40.dp),
                tint = EmeraldGreen
            )
            
            Spacer(modifier = Modifier.width(16.dp))
            
            Column(modifier = Modifier.weight(1f)) {
                Text(
                    text = device.name,
                    style = MaterialTheme.typography.titleMedium,
                    fontWeight = FontWeight.SemiBold
                )
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Text(
                        text = if (device.isOnline) "Online" else "Offline",
                        style = MaterialTheme.typography.bodySmall,
                        color = if (device.isOnline) Success else Color.Gray
                    )
                    if (device.isTrusted) {
                        Spacer(modifier = Modifier.width(8.dp))
                        Icon(
                            Icons.Default.Verified,
                            contentDescription = "Trusted",
                            modifier = Modifier.size(16.dp),
                            tint = EmeraldGreen
                        )
                    }
                }
            }
            
            IconButton(onClick = { /* Options */ }) {
                Icon(Icons.Default.MoreVert, contentDescription = "Options")
            }
        }
    }
}
