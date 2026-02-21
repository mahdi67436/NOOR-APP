package com.noorguard.parent.ui.screens.prayer

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.noorguard.parent.ui.theme.*

data class PrayerTime(
    val name: String,
    val arabicName: String,
    val time: String,
    val isCurrent: Boolean = false
)

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun PrayerTimesScreen(
    onNavigateBack: () -> Unit
) {
    val prayers = listOf(
        PrayerTime("Fajr", "الفجر", "05:30", false),
        PrayerTime("Sunrise", "الشروق", "06:45", false),
        PrayerTime("Dhuhr", "الظهر", "12:30", false),
        PrayerTime("Asr", "العصر", "15:45", true),
        PrayerTime("Maghrib", "المغرب", "18:30", false),
        PrayerTime("Isha", "العشاء", "20:00", false)
    )
    
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Prayer Times", fontWeight = FontWeight.Bold) },
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
        }
    ) { paddingValues ->
        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
                .padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            // Header Card
            item {
                Card(
                    modifier = Modifier.fillMaxWidth(),
                    colors = CardDefaults.cardColors(
                        containerColor = EmeraldGreen
                    )
                ) {
                    Column(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(24.dp),
                        horizontalAlignment = Alignment.CenterHorizontally
                    ) {
                        Text(
                            text = "🕌",
                            style = MaterialTheme.typography.displayMedium
                        )
                        Spacer(modifier = Modifier.height(8.dp))
                        Text(
                            text = "Today's Prayer Times",
                            style = MaterialTheme.typography.titleLarge,
                            color = Color.White,
                            fontWeight = FontWeight.Bold
                        )
                        Text(
                            text = "Mecca, Saudi Arabia",
                            style = MaterialTheme.typography.bodyMedium,
                            color = Color.White.copy(alpha = 0.8f)
                        )
                    }
                }
            }
            
            // Next Prayer
            item {
                Card(
                    modifier = Modifier.fillMaxWidth(),
                    colors = CardDefaults.cardColors(
                        containerColor = Gold.copy(alpha = 0.2f)
                    )
                ) {
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(16.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Icon(
                            Icons.Default.AccessTime,
                            contentDescription = null,
                            tint = Gold,
                            modifier = Modifier.size(32.dp)
                        )
                        Spacer(modifier = Modifier.width(16.dp))
                        Column {
                            Text(
                                "Next Prayer",
                                style = MaterialTheme.typography.bodyMedium,
                                color = MaterialTheme.colorScheme.onSurfaceVariant
                            )
                            Text(
                                "Asr - 03:45 PM",
                                style = MaterialTheme.typography.titleLarge,
                                fontWeight = FontWeight.Bold
                            )
                        }
                    }
                }
            }
            
            // Prayer List
            item {
                Text(
                    "All Prayers",
                    style = MaterialTheme.typography.titleMedium,
                    fontWeight = FontWeight.SemiBold
                )
            }
            
            items(prayers) { prayer ->
                PrayerCard(prayer = prayer)
            }
            
            // Daily Hadith
            item {
                Spacer(modifier = Modifier.height(8.dp))
                Card(
                    modifier = Modifier.fillMaxWidth(),
                    colors = CardDefaults.cardColors(
                        containerColor = MaterialTheme.colorScheme.surfaceVariant
                    )
                ) {
                    Column(
                        modifier = Modifier.padding(16.dp)
                    ) {
                        Text(
                            "📖 Daily Hadith",
                            style = MaterialTheme.typography.titleMedium,
                            fontWeight = FontWeight.Bold
                        )
                        Spacer(modifier = Modifier.height(8.dp))
                        Text(
                            "\"The best among you are those who learn the Quran and teach it to others.\"",
                            style = MaterialTheme.typography.bodyMedium
                        )
                        Text(
                            "- Sahih Bukhari",
                            style = MaterialTheme.typography.bodySmall,
                            color = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                    }
                }
            }
        }
    }
}

@Composable
fun PrayerCard(prayer: PrayerTime) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        colors = CardDefaults.cardColors(
            containerColor = if (prayer.isCurrent) 
                EmeraldGreen.copy(alpha = 0.1f) 
            else MaterialTheme.colorScheme.surface
        )
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Column(modifier = Modifier.weight(1f)) {
                Text(
                    prayer.name,
                    style = MaterialTheme.typography.titleMedium,
                    fontWeight = FontWeight.SemiBold
                )
                Text(
                    prayer.arabicName,
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
            
            Text(
                prayer.time,
                style = MaterialTheme.typography.titleLarge,
                fontWeight = FontWeight.Bold,
                color = if (prayer.isCurrent) EmeraldGreen else MaterialTheme.colorScheme.onSurface
            )
            
            if (prayer.isCurrent) {
                Spacer(modifier = Modifier.width(8.dp))
                Icon(
                    Icons.Default.CheckCircle,
                    contentDescription = "Current",
                    tint = EmeraldGreen
                )
            }
        }
    }
}
