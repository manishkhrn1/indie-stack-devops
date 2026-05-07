using UnityEngine;
using UnityEngine.Networking;
using System.Collections;
using System.Text;

public class IndieStackManager : MonoBehaviour
{
    // The URL where your Docker container is running
    private string baseUrl = "http://localhost:5000";

    public static IndieStackManager Instance;

    private void Awake() {
        Instance = this;
    }

    public void UploadScore(string playerName, int score, int level) {
        StartCoroutine(PostScore(playerName, score, level));
    }

    private IEnumerator PostScore(string playerName, int score, int level) {
        string json = $"{{\"player_name\": \"{playerName}\", \"score\": {score}, \"level\": {level}}}";
        
        using (UnityWebRequest request = new UnityWebRequest(baseUrl + "/update_stats", "POST")) {
            byte[] bodyRaw = Encoding.UTF8.GetBytes(json);
            request.uploadHandler = new UploadHandlerRaw(bodyRaw);
            request.downloadHandler = new DownloadHandlerBuffer();
            request.SetRequestHeader("Content-Type", "application/json");

            yield return request.SendWebRequest();

            if (request.result != UnityWebRequest.Result.Success) {
                Debug.LogError("IndieStack Error: " + request.error);
            } else {
                Debug.Log("IndieStack Success: Stats Synced!");
            }
        }
    }
}