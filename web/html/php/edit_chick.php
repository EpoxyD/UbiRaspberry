<?php
/**
 * Created by IntelliJ IDEA.
 * User: Max
 * Date: 24/03/2017
 * Time: 09:50
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

if (isset($_GET['id'])) {
    $id = $_GET['id'];
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
 *        Set chick          *
 *****************************/

$sql = "UPDATE ChickCounter.chickens SET name = '$name', race = '$race', age = '$age', imagepath = '$imgPath' WHERE id = '$id';";

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
$array[] = array(
    "status" => "succes"
);

echo json_encode($array);

?>