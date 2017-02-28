import com.pi4j.component.switches.SwitchListener;
import com.pi4j.component.switches.SwitchState;
import com.pi4j.component.switches.SwitchStateChangeEvent;
import com.pi4j.device.piface.PiFace;
import com.pi4j.device.piface.PiFaceLed;
import com.pi4j.device.piface.PiFaceRelay;
import com.pi4j.device.piface.PiFaceSwitch;
import com.pi4j.device.piface.impl.PiFaceDevice;
import com.pi4j.io.spi.SpiChannel;
import com.pi4j.wiringpi.GpioUtil;
import com.pi4j.io.gpio.*;

import java.io.IOException;
import java.util.Scanner;

public class Demo {

    public static void main(String args[]) throws InterruptedException, IOException {

        // Enable NonPrivilegedAccess to be able to run the Java Class without 'sudo'
        // *** will disable some other features ***
        GpioUtil.enableNonPrivilegedAccess();
        final GpioController gpio = GpioFactory.getInstance();

        // create the Pi-Face controller
        final PiFace piface = new PiFaceDevice(PiFace.DEFAULT_ADDRESS, SpiChannel.CS0);

        piface.getSwitch(PiFaceSwitch.S1).addListener(new SwitchListener() {
            @Override
            public void onStateChange(SwitchStateChangeEvent event) {
                if(event.getNewState() == SwitchState.ON){;
                    piface.getRelay(PiFaceRelay.K0).close(); // turn on relay
                }
                else{
                    piface.getRelay(PiFaceRelay.K0).open(); // turn off relay
                }
            }
        });

        Scanner sc = new Scanner(System.in);
        while(sc.hasNext()) {
            String command = sc.nextLine();
            if (command.trim().equals("q")) {
                break;
            }
        }
        
        gpio.shutdown();
        System.exit(0);
    }
}

