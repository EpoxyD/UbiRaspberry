<?php

// autoload_static.php @generated by Composer

namespace Composer\Autoload;

class ComposerStaticInitb23b4628c1d3514a9d4e7adc9ee4a6f0
{
    public static $prefixesPsr0 = array (
        'P' => 
        array (
            'Pkj\\Raspberry\\PiFace' => 
            array (
                0 => __DIR__ . '/..' . '/pkj/raspberry-piface-api/src',
            ),
        ),
    );

    public static function getInitializer(ClassLoader $loader)
    {
        return \Closure::bind(function () use ($loader) {
            $loader->prefixesPsr0 = ComposerStaticInitb23b4628c1d3514a9d4e7adc9ee4a6f0::$prefixesPsr0;

        }, null, ClassLoader::class);
    }
}
