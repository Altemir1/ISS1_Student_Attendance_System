<?php
if (isset($_GET["uid"])) {
   $uid = $_GET["uid"]; // Get UID from HTTP GET parameter
   $current_time = date("Y-m-d H:i:s"); // Get current time

   // Database configuration
   $servername = "localhost";
   $username = "ESP32";
   $password = "esp32io.com";
   $database_name = "card_readerv2";

   // Create MySQL connection
   $connection = new mysqli($servername, $username, $password, $database_name);
   // Check connection
   if ($connection->connect_error) {
      die("MySQL connection failed: " . $connection->connect_error);
   }

   // Prepare the SQL statement with a parameterized query to prevent SQL injection
   $sql = "INSERT INTO student_action (STUDENT_ID, DATA) VALUES (?, ?)";
   $statement = $connection->prepare($sql);

   // Bind the parameters to the statement
   $statement->bind_param("ss", $uid, $current_time);

   // Execute the statement
   if ($statement->execute()) {
      echo "New record created successfully";
   } else {
      echo "Error: " . $sql . " => " . $connection->error;
   }

   // Close the statement and connection
   $statement->close();
   $connection->close();
} else {
   echo "UID is not set in the HTTP request";
}
?>
