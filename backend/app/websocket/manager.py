"""
NoorGuard Ultimate - WebSocket Manager
Real-time Communication for Live Updates
"""

from typing import Dict, Set, Optional
from fastapi import WebSocket, WebSocketDisconnect
import json
import asyncio
from datetime import datetime
import uuid


class ConnectionManager:
    """WebSocket connection manager for real-time updates"""
    
    def __init__(self):
        # Active connections by user_id
        self.active_connections: Dict[str, Set[WebSocket]] = {}
        # Connection metadata
        self.connection_info: Dict[WebSocket, dict] = {}
    
    async def connect(self, websocket: WebSocket, user_id: str, device_id: Optional[str] = None):
        """Connect a new WebSocket client"""
        await websocket.accept()
        
        if user_id not in self.active_connections:
            self.active_connections[user_id] = set()
        
        self.active_connections[user_id].add(websocket)
        
        self.connection_info[websocket] = {
            "user_id": user_id,
            "device_id": device_id,
            "connected_at": datetime.utcnow(),
            "client": websocket.client.host if websocket.client else "unknown"
        }
        
        # Send connection confirmation
        await self.send_personal_message({
            "type": "connection",
            "status": "connected",
            "user_id": user_id,
            "timestamp": datetime.utcnow().isoformat()
        }, websocket)
    
    def disconnect(self, websocket: WebSocket, user_id: str):
        """Disconnect a WebSocket client"""
        if user_id in self.active_connections:
            self.active_connections[user_id].discard(websocket)
            
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]
        
        if websocket in self.connection_info:
            del self.connection_info[websocket]
    
    async def send_personal_message(self, message: dict, websocket: WebSocket):
        """Send message to a specific WebSocket"""
        try:
            await websocket.send_text(json.dumps(message))
        except Exception:
            pass
    
    async def send_to_user(self, user_id: str, message: dict):
        """Send message to all connections for a user"""
        if user_id in self.active_connections:
            disconnected = set()
            
            for connection in self.active_connections[user_id]:
                try:
                    await connection.send_text(json.dumps(message))
                except Exception:
                    disconnected.add(connection)
            
            # Clean up disconnected
            for conn in disconnected:
                self.disconnect(conn, user_id)
    
    async def broadcast(self, message: dict, exclude_users: list = None):
        """Broadcast message to all connected users"""
        exclude_users = exclude_users or []
        
        for user_id, connections in self.active_connections.items():
            if user_id in exclude_users:
                continue
            
            for connection in connections:
                try:
                    await connection.send_text(json.dumps(message))
                except Exception:
                    pass
    
    def get_connected_users(self) -> list:
        """Get list of connected user IDs"""
        return list(self.active_connections.keys())
    
    def get_connection_count(self) -> int:
        """Get total number of connections"""
        return sum(len(conns) for conns in self.active_connections.values())


# Global WebSocket manager
manager = ConnectionManager()


# WebSocket message types
class MessageType:
    """WebSocket message types"""
    # Connection
    CONNECTION = "connection"
    PING = "ping"
    PONG = "pong"
    
    # Device updates
    DEVICE_STATUS = "device_status"
    DEVICE_LOCATION = "device_location"
    DEVICE_LOCK = "device_lock"
    DEVICE_UNLOCK = "device_unlock"
    
    # Activity
    ACTIVITY_LOG = "activity_log"
    BLOCKED_ATTEMPT = "blocked_attempt"
    SCREEN_TIME_UPDATE = "screen_time_update"
    
    # Alerts
    ALERT = "alert"
    EMERGENCY = "emergency"
    ANOMALY_DETECTED = "anomaly_detected"
    
    # Islamic
    PRAYER_TIME = "prayer_time"
    PRAYER_REMINDER = "prayer_reminder"
    DAILY_HADITH = "daily_hadith"
    
    # Sync
    SYNC_REQUEST = "sync_request"
    SYNC_RESPONSE = "sync_response"


async def handle_websocket_client(websocket: WebSocket, user_id: str, device_id: Optional[str] = None):
    """Handle WebSocket client connection and messages"""
    await manager.connect(websocket, user_id, device_id)
    
    try:
        while True:
            # Wait for messages
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Handle ping
            if message.get("type") == MessageType.PING:
                await manager.send_personal_message({
                    "type": MessageType.PONG,
                    "timestamp": datetime.utcnow().isoformat()
                }, websocket)
            
            # Handle sync request
            elif message.get("type") == MessageType.SYNC_REQUEST:
                # Process sync request and send response
                await manager.send_personal_message({
                    "type": MessageType.SYNC_RESPONSE,
                    "data": {},
                    "timestamp": datetime.utcnow().isoformat()
                }, websocket)
            
            # Handle other message types
            else:
                # Process other message types as needed
                pass
                
    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)
    except Exception as e:
        print(f"WebSocket error: {e}")
        manager.disconnect(websocket, user_id)


# Notification helper functions
async def notify_parent_alert(parent_id: str, child_id: str, alert_type: str, message: str, data: dict = None):
    """Send alert notification to parent"""
    await manager.send_to_user(parent_id, {
        "type": MessageType.ALERT,
        "alert_type": alert_type,
        "child_id": child_id,
        "message": message,
        "data": data or {},
        "timestamp": datetime.utcnow().isoformat()
    })


async def notify_device_status(device_id: str, status: str):
    """Send device status update"""
    await manager.send_to_user(device_id, {
        "type": MessageType.DEVICE_STATUS,
        "status": status,
        "timestamp": datetime.utcnow().isoformat()
    })


async def broadcast_prayer_time(prayer_times: dict):
    """Broadcast prayer time updates to all users"""
    await manager.broadcast({
        "type": MessageType.PRAYER_TIME,
        "prayer_times": prayer_times,
        "timestamp": datetime.utcnow().isoformat()
    })
