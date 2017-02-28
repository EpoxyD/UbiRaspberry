<?php
//include and use myPHPiFace library
use Pkj\Raspberry\PiFace\PiFaceDigital;
require 'myphpiface/vendor/autoload.php';

$dev = PiFaceDigital::create();
// Run once. (clear all outputs)
$dev->init();

//turn on LED0
$dev->getLeds()[0]->turnOn(); 
