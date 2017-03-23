<?php
/**
 * Created by IntelliJ IDEA.
 * User: Max
 * Date: 23/03/2017
 * Time: 10:42
 */

include('db_config.php');


$mysqli = new mysqli($host, $user, $password, $db);
if ($mysqli->connect_errno) {
    // The connection failed. What do you want to do?
    // You could contact yourself (email?), log the error, show a nice page, etc.
    // You do not want to reveal sensitive information

    // Let's try this:
    echo "Sorry, this website is experiencing problems.";

    // Something you should not do on a public site, but this example will show you
    // anyways, is print out MySQL error related information -- you might log this
    echo "Error: Failed to make a MySQL connection, here is why: \n";
    echo "Errno: " . $mysqli->connect_errno . "\n";
    echo "Error: " . $mysqli->connect_error . "\n";

    // You might want to show them something nice, but we will simply exit
    exit;
}

$sql = "SELECT * FROM ChickCounter.chickens";
if (!$result = $mysqli->query($sql)) {

    echo "Error: Failed to execute query: \n";
    echo "Query: " . $sql . "\n";
    echo "Errno: " . $mysqli->errno . "\n";
    echo "Error: " . $mysqli->error . "\n";
    exit;
}

$chickens =  array();
while ($chick = $result->fetch_assoc()) {
    $chickens[] = $chick;
}

echo json_encode($chickens);

?>