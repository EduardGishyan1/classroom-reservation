from quart import Blueprint, jsonify, websocket
import aiohttp
import json

from app.services.active_connections import active_connections
from app.schemas.student import BookingNotification

from app.config.settings import settings


router = Blueprint("students",__name__,url_prefix="/students")

@router.route("/send-message", methods=["POST"])
async def send_message_to_slack():
  try:
    async with aiohttp.ClientSession() as session:
      async with session.post(
        'https://slack.com/api/chat.postMessage',
        headers={"Authorization": f"Bearer {settings.SLACK_BOT_TOKEN}"},
        json={
          "channel": "#random",
          "text": "Slack integration to classroom project"
        }) as response:
        if response.status == 200:
          response_data = await response.json()
          if response_data.get("ok"):
            return jsonify({"message": "Message sent to Slack successfully!"}), 200
          else:
            error_message = response_data.get("error", "Unknown error")
            return jsonify({"error": f"Slack API error: {error_message}"}), 400
        else:
          error_response = await response.json()
          return jsonify({"error": "Failed to send message to Slack", "details": error_response}), 400

  except aiohttp.ClientError as e:
    return jsonify({"error": f"Error sending message to Slack: {e}"}), 500
  except Exception as e:
    return jsonify({"error": f"Unexpected error: {e}"}), 500
  
@router.websocket("/student-ws")
async def student_ws_connection():
    conn = websocket._get_current_object()
    active_connections.add(conn)
    try:
        while True:
            message = await websocket.receive()
            try:
              message_dict = json.loads(message)
              data = BookingNotification(**message_dict)
            except:
                await websocket.send_json({"error": "Invalid arguments"})
                continue
            data = data.model_dump()
            await broadcast_to_admins(f"Notification from Student: {data}")

    except Exception as e:
        await websocket.send_json({"error": f"Error with WebSocket connection: {str(e)}"})
    finally:
        active_connections.remove(conn)
     
async def broadcast_to_admins(message: str):
    for conn in list(active_connections): 
        try:
            await conn.send(message)
        except Exception:
            active_connections.remove(conn)  