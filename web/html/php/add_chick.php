<?php
/**
 * Created by IntelliJ IDEA.
 * User: Max
 * Date: 23/03/2017
 * Time: 11:13
 */

include('db_config.php');

/*****************************
 *       Get Variables       *
 *****************************/

if (isset($_GET['name'])) {
    $name = $_GET['name'];
}

if (isset($_GET['race'])) {
    $race = $_GET['race'];
}

if (isset($_GET['age'])) {
    $age = $_GET['age'];
}

if (isset($_GET['imgPath'])) {
    $imgPath = $_GET['imgPath'];
}

/*****************************
 *       Connect to db       *
 *****************************/


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

/*****************************
 *        Set chick        *
 *****************************/

$sql = "INSERT INTO ChickCounter.chickens (name, race, age, imagepath)
                            VALUES ('$name', '$race', '$age', '$imgPath');";
$result = $mysqli->query($sql);

if(!$result) {
    echo "Error: Failed to execute query: \n";
    echo "Query: " . $sql . "\n";
    echo "Errno: " . $mysqli->errno . "\n";
    echo "Error: " . $mysqli->error . "\n";
    exit;
}

/******************************
 *       get chick ID       *
 ******************************/

$newChickId = $mysqli->insert_id;

/******************************
 *         store Img          *
 ******************************/

rename("/var/www/html/uploads/chick_add.png", "/var/www/html/uploads/chick_" . $newChickId . ".png");
$imgPath = "uploads/chick_" . $newChickId . ".png";

$sql = "UPDATE ChickCounter.chickens SET imagepath = '$imgPath' WHERE id = '$newChickId';";
$result = $mysqli->query($sql);

if(!$result) {
    echo "Error: Failed to execute query: \n";
    echo "Query: " . $sql . "\n";
    echo "Errno: " . $mysqli->errno . "\n";
    echo "Error: " . $mysqli->error . "\n";
    exit;
}

/******************************
 *           Succes           *
 ******************************/

$array[] = $newChickId;
$array[] = $imgPath;
$array[] = array(
    "status" => "succes"
);

echo json_encode($array);

?>