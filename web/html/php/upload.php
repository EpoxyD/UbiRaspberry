<?php
/*
    echo '<pre>';
    print_r($_FILES);
    echo '</pre>';

    $target_dir = "/var/www/html/uploads/";
    $target_file = $target_dir . basename("chick_" . $_POST['chick_id'] . ".png");
    echo $target_file;
    $uploadOk = 1;
    $imageFileType = pathinfo($target_file,PATHINFO_EXTENSION);
    // Check if image file is a actual image or fake image
    if(isset($_POST["submit"])) {
        $check = getimagesize($_FILES["fileToUpload"]["tmp_name"]);
        if($check !== false) {
            echo "File is an image - " . $check["mime"] . ".";
            $uploadOk = 1;
        } else {
            echo "File is not an image.";
            $uploadOk = 0;
        }
    }

    // Check file size
    if ($_FILES["fileToUpload"]["size"] > 500000) {
        echo "Sorry, your file is too large.";
        $uploadOk = 0;
    }
    // Allow certain file formats
    if($imageFileType != "jpg" && $imageFileType != "png" && $imageFileType != "jpeg"
        && $imageFileType != "gif" ) {
        echo "Sorry, only JPG, JPEG, PNG & GIF files are allowed.";
        $uploadOk = 0;
    }
    // Check if $uploadOk is set to 0 by an error
    if ($uploadOk == 0) {
        echo "Sorry, your file was not uploaded.";
    // if everything is ok, try to upload file
    } else {
        if (move_uploaded_file($_FILES["fileToUpload"]["tmp_name"], $target_file)) {
            echo "The file ". basename( $_FILES["fileToUpload"]["name"]). " has been uploaded.";
        } else {
            echo "Sorry, there was an error uploading your file.";
        }
    }
*/


$ds          = DIRECTORY_SEPARATOR;  //1

$storeFolder = '/var/www/html/uploads';   //2

if (!empty($_FILES)) {

    $tempFile = $_FILES['file']['tmp_name'];          //3

    $targetPath = $storeFolder . $ds;  //4

    $targetFile =  $targetPath. basename("chick_" . $_POST['chick_id'] . ".png");  //5

    move_uploaded_file($tempFile,$targetFile); //6



    if ($_POST['chick_id'] != "add"){
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

        $id = $_POST['chick_id'];
        $imgPath = "uploads/" . basename("chick_" . $_POST['chick_id'] . ".png");

        $sql = "UPDATE ChickCounter.chickens SET imagepath = '$imgPath' WHERE id = '$id';";

        $result = $mysqli->query($sql);

        if(!$result) {
            echo "Error: Failed to execute query: \n";
            echo "Query: " . $sql . "\n";
            echo "Errno: " . $mysqli->errno . "\n";
            echo "Error: " . $mysqli->error . "\n";
            exit;
        }
    }

}

?>