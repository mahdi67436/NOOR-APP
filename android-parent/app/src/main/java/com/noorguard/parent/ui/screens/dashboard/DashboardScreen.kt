package com.noorguard.parent.ui.screens.dashboard

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.launch
import javax.inject.Inject
import com.noorguard.parent.ui.theme.*

data class ChildInfo(
    val id: String,
    val name: String,
    val avatar: String,
    val isOnline: Boolean,
    val riskScore: Int,
    val screenTime: String
)

data class DashboardStat(
    val title: String,
    val value: String,
    val icon: ImageVector,
    val color: Color
)

@HiltViewModel
class DashboardViewModel @Inject constructor() : ViewModel() {
    var children by mutableStateOf(listOf(
        ChildInfo("1", "Ahmed", "👦", true, 25, "2h 30m"),
        ChildInfo("2", "Fatima", "👧", true, 15, "1h 45m"),
        ChildInfo("3", "Omar", "👦", false, 45, "3h 15m")
    ))
    
    var stats by mutableStateOf(listOf(
        DashboardStat("Total Children", "3", Icons.Default.People, EmeraldGreen),
        DashboardStat("Online Now", "2", Icons.Default.PhoneAndroid, Success),
        DashboardStat("Blocked Today", "12", Icons.Default.Block, Warning),
        DashboardStat("Risk Alerts", "1", Icons.Default.Warning, Error)
    ))
    
    var isLoading by mutableStateOf(false)
    
    fun refresh() {
        viewModelScope.launch {
            isLoading = true
            kotlinx.coroutines.delay(1000)
            isLoading = false
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun DashboardScreen(
    onNavigateToDevices: () -> Unit,
    onNavigateToChildren: () -> Unit,
    onNavigateToAnalytics: () -> Unit,
    onNavigateToSettings: () -> Unit,
    onNavigateToPrayer: () -> Unit,
    viewModel: DashboardViewModel = hiltViewModel()
) {
    Scaffold(
        topBar = {
            TopAppBar(
                title = { 
                    Column {
                        Text("NoorGuard", fontWeight = FontWeight.Bold)
                        Text(
                            "Welcome back!", 
                            style = MaterialTheme.typography.bodySmall,
                            color = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                    }
                },
                actions = {
                    IconButton(onClick = { viewModel.refresh() }) {
                        Icon(Icons.Default.Refresh, contentDescription = "Refresh")
                    }
                    IconButton(onClick = onNavigateToSettings) {
                        Icon(Icons.Default.Settings, contentDescription = "Settings")
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = EmeraldGreen,
                    titleContentColor = Color.White,
                    actionIconContentColor = Color.White
                )
            )
        }
    ) { paddingValues ->
        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
                .padding(horizontal = 16.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            item { Spacer(modifier = Modifier.height(8.dp)) }
            
            // Stats Row
            item {
                LazyRow(
                    horizontalArrangement = Arrangement.spacedBy(12.dp)
                ) {
                    items(viewModel.stats) { stat ->
                        StatCard(stat = stat)
                    }
                }
            }
            
            // Quick Actions
            item {
                Text(
                    text = "Quick Actions",
                    style = MaterialTheme.typography.titleMedium,
                    fontWeight = FontWeight.SemiBold
                )
            }
            
            item {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.spacedBy(12.dp)
                ) {
                    QuickActionCard(
                        modifier = Modifier.weight(1f),
                        icon = Icons.Default.Devices,
                        title = "Devices",
                        color = EmeraldGreen,
                        onClick = onNavigateToDevices
                    )
                    QuickActionCard(
                        modifier = Modifier.weight(1f),
                        icon = Icons.Default.ChildCare,
                        title = "Children",
                        color = Gold,
                        onClick = onNavigateToChildren
                    )
                }
            }
            
            item {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.spacedBy(12.dp)
                ) {
                    QuickActionCard(
                        modifier = Modifier.weight(1f),
                        icon = Icons.Default.Analytics,
                        title = "Analytics",
                        color = Info,
                        onClick = onNavigateToAnalytics
                    )
                    QuickActionCard(
                        modifier = Modifier.weight(1f),
                        icon = Icons.Default.Mosque,
                        title = "Prayer",
                        color = EmeraldGreenDark,
                        onClick = onNavigateToPrayer
                    )
                }
            }
            
            // Children Status
            item {
                Text(
                    text = "Children Status",
                    style = MaterialTheme.typography.titleMedium,
                    fontWeight = FontWeight.SemiBold
                )
            }
            
            items(viewModel.children) { child ->
                ChildStatusCard(child = child)
            }
            
            item { Spacer(modifier = Modifier.height(16.dp)) }
        }
    }
}

@Composable
fun StatCard(stat: DashboardStat) {
    Card(
        modifier = Modifier.width(150.dp),
        colors = CardDefaults.cardColors(
            containerColor = MaterialTheme.colorScheme.surface
        ),
        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
    ) {
        Column(
            modifier = Modifier.padding(16.dp)
        ) {
            Icon(
                imageVector = stat.icon,
                contentDescription = null,
                tint = stat.color,
                modifier = Modifier.size(24.dp)
            )
            Spacer(modifier = Modifier.height(8.dp))
            Text(
                text = stat.value,
                style = MaterialTheme.typography.headlineSmall,
                fontWeight = FontWeight.Bold
            )
            Text(
                text = stat.title,
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        }
    }
}

@Composable
fun QuickActionCard(
    modifier: Modifier = Modifier,
    icon: ImageVector,
    title: String,
    color: Color,
    onClick: () -> Unit
) {
    Card(
        modifier = modifier
            .height(100.dp)
            .clickable(onClick = onClick),
        colors = CardDefaults.cardColors(
            containerColor = color.copy(alpha = 0.1f)
        )
    ) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(16.dp),
            verticalArrangement = Arrangement.Center,
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Icon(
                imageVector = icon,
                contentDescription = null,
                tint = color,
                modifier = Modifier.size(32.dp)
            )
            Spacer(modifier = Modifier.height(8.dp))
            Text(
                text = title,
                style = MaterialTheme.typography.titleSmall,
                fontWeight = FontWeight.Medium
            )
        }
    }
}

@Composable
fun ChildStatusCard(child: ChildInfo) {
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
            // Avatar
            Box(
                modifier = Modifier
                    .size(50.dp)
                    .clip(CircleShape)
                    .background(EmeraldGreen.copy(alpha = 0.2f)),
                contentAlignment = Alignment.Center
            ) {
                Text(
                    text = child.avatar,
                    style = MaterialTheme.typography.headlineSmall
                )
            }
            
            Spacer(modifier = Modifier.width(16.dp))
            
            // Info
            Column(modifier = Modifier.weight(1f)) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Text(
                        text = child.name,
                        style = MaterialTheme.typography.titleMedium,
                        fontWeight = FontWeight.SemiBold
                    )
                    Spacer(modifier = Modifier.width(8.dp))
                    Box(
                        modifier = Modifier
                            .size(8.dp)
                            .clip(CircleShape)
                            .background(if (child.isOnline) Success else Color.Gray)
                    )
                }
                Text(
                    text = "Screen time: ${child.screenTime}",
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
            
            // Risk Score
            Column(horizontalAlignment = Alignment.CenterHorizontally) {
                Text(
                    text = "${child.riskScore}",
                    style = MaterialTheme.typography.titleLarge,
                    fontWeight = FontWeight.Bold,
                    color = when {
                        child.riskScore < 25 -> RiskLow
                        child.riskScore < 50 -> RiskMedium
                        child.riskScore < 75 -> RiskHigh
                        else -> RiskCritical
                    }
                )
                Text(
                    text = "Risk",
                    style = MaterialTheme.typography.labelSmall
                )
            }
        }
    }
}
