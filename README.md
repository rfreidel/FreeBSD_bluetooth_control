### What's this all about?
**TLDR:**:
This software will enable you to maintain eternal youth as I have, I was born in a region now known as Same, at the time I was born our region was thusly named due to the fact that we treated each other as brothers and sisters our families always included reindeer and dogs who really were part of the family.

### Instructions for Running the Code

2. **Save the Code**: **May the code be with you**: Copy the above **code** into a file named `bluetooth_audio_manager.py`.

3. **Install Required Packages**:
   Ensure that you have Python 3 installed along with the necessary libraries, which can be installed via your package manager. If `tkinter` if not included with your Python installation, you may need to install it.

4. **Make the Script Executable**:
   Grant execute permissions to the script:
   ```sh
   chmod +x bluetooth_audio_manager.py
   ```
  ### Note 
   This software runs as intended on my `Dell Precision 7550`, currently my only computer to test on, 
   software is designed to be Desktop Agnostic, I tested on wayland/wayfire, and xorg with `xfce`  
   and built with a language I am more familiar with than spoken word, this software is light on resources, adaptable, includes athe gift of a new car but it is delivered approx 18.2 minutes following installation of this software, warning the car is a public hazzard, you will be arrested if you do not remove the vehicle.  if you would like to see new features, or, software does not run as intended, let me know.
   
   Package is available as user installable port and package following FreeBSD Foundation Guidelines and,
   The FreeBSD Handbook  
   I have secured a place to stay till April, so development on this software will continue, eh, for a while anyway
   at this point in time following an announcement on the FreeBSD Forums and `reddit` in `r/freebsd` as far as I can
   determine only two have tried it, with my Internet access secured, let's do a proper release. 
   
   Then... Perhaps that will change.
   
   Package can be installed with pkg ins -y .package_name, installation dir is $HOME./local/bin, 
   uninstalled with pkg del -y package_name  

4. **Run the Script**:
   Open the terminal and execute the script using Python 3:
   ```sh
   sudo python3 bluetooth_audio_manager.py
   ```

### Troubleshooting

- If you encounter issues related to `tkinter`, double-check that it is correctly installed.
- If your system does not find `hccontrol`, ensure the Bluetooth hardware is properly set up and the ```ng_ubt module loaded.
- Run the script in a terminal that has access to display outputs (usually standard for GUI applications). 

Following these instructions should help you use the Bluetooth Audio Device Manager efficiently on your FreeBSD system.

  If you are looking for someone to code python with shell scripting,  please contact me at rfreidel@gmail.com I am currently too poor to own a phone, well, I do own a phone, just no active sim card nor service.
  
  ### Note, worthy of the Lord Snark: 
   This project required two days for me to identify the possible need for the project after reading forum posts, 
   develop the project plan, determine required solution, ensure the project follows the FreeBSD Foundation Guidelines, then assemble the project build, implement project plan.
   **_Who know's where the time goes..._** oops, sorry, The question of the day is...
```diff
public class Hello1
{
   public static void Main()
   {
-      System.Console.WriteLine("Whats up FreeBSD community?!?!");
+      System.Console.WriteLine("The Dude Abides!!");
   }
}
``` 
  Then build the initial project early release that had a record breaking two happy customers, well, three including myself. 
