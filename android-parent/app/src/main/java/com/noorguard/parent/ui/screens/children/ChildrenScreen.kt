package com.noorguard.parent.ui.screens.children

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.ViewModel
import dagger.hilt.android.lifecycle.HiltViewModel
import javax.inject.Inject
import com.noorguard.parent.ui.theme.*

@HiltViewModel
class ChildrenViewModel @Inject constructor() : ViewModel() {
    var children = listOf(
        ChildItem("1", "Ahmed", "👦", true, 12, "moderate"),
        ChildItem("2", "Fatima", "👧", true, 10, "strict"),
        ChildItem("3", "Omar", "👦", false, 8, "minimal")
    )
}

data class ChildItem(
    val id: String,
    val name: String,
    val avatar: String,
    val isOnline: Boolean,
    val age: Int,
    val filterLevel: String
)

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ChildrenScreen(
    onNavigateToChild: (String) -> Unit,
    onNavigateBack: () -> Unit,
    viewModel: ChildrenViewModel = hiltViewModel()
) {
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Children", fontWeight = FontWeight.Bold) },
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
                onClick = { /* Add child */ },
                containerColor = EmeraldGreen
            ) {
                Icon(Icons.Default.Add, contentDescription = "Add Child")
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
            items(viewModel.children) { child ->
                ChildCard(
                    child = child,
                    onClick = { onNavigateToChild(child.id) }
                )
            }
        }
    }
}

@Composable
fun ChildCard(
    child: ChildItem,
    onClick: () -> Unit
) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .clickable(onClick = onClick),
        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Box(
                modifier = Modifier
                    .size(56.dp)
                    .clip(CircleShape)
                    .background(EmeraldGreen.copy(alpha = 0.2f)),
                contentAlignment = Alignment.Center
            ) {
                Text(text = child.avatar, style = MaterialTheme.typography.headlineSmall)
            }
            
            Spacer(modifier = Modifier.width(16.dp))
            
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
                    text = "Age: ${child.age} | Filter: ${child.filterLevel}",
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
            
            Icon(Icons.Default.ChevronRight, contentDescription = null)
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ChildDetailScreen(
    childId: String,
    onNavigateBack: () -> Unit
) {
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Child Details", fontWeight = FontWeight.Bold) },
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
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
                .padding(16.dp)
        ) {
            Text("Child ID: $childId")
            // Add child details here
        }
    }
}
