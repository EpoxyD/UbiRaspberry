<?php
/**
 * Created by IntelliJ IDEA.
 * User: Max
 * Date: 06/03/2017
 * Time: 14:40
 */

error_reporting(E_ALL);
ini_set('display_errors', TRUE);
ini_set('display_startup_errors', TRUE);

var_dump($_FILES);
if (!empty($_FILES) && isset($_FILES['fileToUpload'])) {
    switch ($_FILES['fileToUpload']["error"]) {
        case UPLOAD_ERR_OK:
            $target = "uploads/";
            $target = $target . basename($_FILES['fileToUpload']['name']);

            if (move_uploaded_file($_FILES['fileToUpload']['tmp_name'], $target)) {
                $status = "The file " . basename($_FILES['fileToUpload']['name']) . " has been uploaded";
                $imageFileType = pathinfo($target, PATHINFO_EXTENSION);
                $check = getimagesize($target);
                if ($check !== false) {
                    echo "File is an image - " . $check["mime"] . ".<br>";
                    $uploadOk = 1;
                } else {
                    echo "File is not an image.<br>";
                    $uploadOk = 0;
                }

            } else {
                $status = "Sorry, there was a problem uploading your file.";
            }
            break;

    }

    echo "Status: {$status}<br/>\n";

}