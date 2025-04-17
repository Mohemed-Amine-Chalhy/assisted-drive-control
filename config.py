import tkinter as tk
from tkinter import ttk
import serial.tools.list_ports

class ControlPanel:
    def __init__(self, root):
        self.root = root
        self.root.title("System Control Panel")
        self.root.geometry("800x600")
        self.root.configure(bg="#f5f5f5")
        
        # Variables
        self.lidar_active = False
        self.camera_active = False
        self.stop_assist_active = False
        
        # Main container
        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create a notebook with tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_sensor_tab()
        self.create_motor_tab()
        
        # Status bar
        status_frame = ttk.Frame(root, relief=tk.SUNKEN )
        status_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=10 )
        self.status_label = ttk.Label(status_frame, text="System ready" )
        self.status_label.pack(side=tk.LEFT, pady=5, padx=10)
        
    #     # Apply custom styles
    #     self.apply_styles()
    
    # def apply_styles(self):
    #     # Create custom style
    #     style = ttk.Style()
    #     style.configure('TFrame', background='#f5f5f5')
    #     style.configure('TLabel', background='#f5f5f5', font=('Arial', 10))
    #     style.configure('TButton', font=('Arial', 10))
    #     style.configure('Header.TLabel', font=('Arial', 12, 'bold'))
    #     style.configure('Section.TFrame', background='#e1e1e1', relief='raised')
        
    #     # Configure button styles
    #     style.configure('Activate.TButton', background='#4CAF50', foreground='white')
    #     style.configure('Deactivate.TButton', background='#f44336', foreground='white')
        
    def create_sensor_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Sensors & Assist")
        
        # LIDAR Section
        lidar_frame = ttk.LabelFrame(tab, text="LIDAR Settings", padding="10")
        lidar_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # LIDAR Port Row
        port_frame = ttk.Frame(lidar_frame)
        port_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(port_frame, text="Port:").pack(side=tk.LEFT, padx=(0, 10))
        
        lidar_port_var = tk.StringVar(value="COM6")
        lidar_port = ttk.Combobox(port_frame, textvariable=lidar_port_var, width=10)
        lidar_port['values'] = ('COM6', 'COM7', 'COM8', 'COM9')
        lidar_port.pack(side=tk.LEFT)
        
        # LIDAR Control Row
        control_frame = ttk.Frame(lidar_frame)
        control_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(control_frame, text="Status:").pack(side=tk.LEFT, padx=(0, 10))
        
        self.lidar_status = ttk.Label(control_frame, text="Inactive", foreground="red")
        self.lidar_status.pack(side=tk.LEFT, padx=(0, 20))
        
        activate_lidar_btn = ttk.Button(control_frame, text="Activate LIDAR", 
                                        command=self.toggle_lidar, style='Activate.TButton')
        activate_lidar_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        deactivate_lidar_btn = ttk.Button(control_frame, text="Deactivate LIDAR", 
                                          command=self.toggle_lidar, style='Deactivate.TButton')
        deactivate_lidar_btn.pack(side=tk.LEFT)
        
        # Camera Section
        camera_frame = ttk.LabelFrame(tab, text="Camera Settings", padding="10")
        camera_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Camera Port Row
        port_frame = ttk.Frame(camera_frame)
        port_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(port_frame, text="Port:").pack(side=tk.LEFT, padx=(0, 10))
        
        camera_port_var = tk.StringVar(value="COM7")
        camera_port = ttk.Combobox(port_frame, textvariable=camera_port_var, width=10)
        camera_port['values'] = ('COM6', 'COM7', 'COM8', 'COM9')
        camera_port.pack(side=tk.LEFT)
        
        # Camera Control Row
        control_frame = ttk.Frame(camera_frame)
        control_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(control_frame, text="Status:").pack(side=tk.LEFT, padx=(0, 10))
        
        self.camera_status = ttk.Label(control_frame, text="Inactive", foreground="red")
        self.camera_status.pack(side=tk.LEFT, padx=(0, 20))
        
        activate_camera_btn = ttk.Button(control_frame, text="Activate Camera", 
                                         command=self.toggle_camera, style='Activate.TButton')
        activate_camera_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        deactivate_camera_btn = ttk.Button(control_frame, text="Deactivate Camera", 
                                           command=self.toggle_camera, style='Deactivate.TButton')
        deactivate_camera_btn.pack(side=tk.LEFT)
        
        # Stop Assist Section
        assist_frame = ttk.LabelFrame(tab, text="Stop Assist", padding="10")
        assist_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Stop Assist Control Row
        control_frame = ttk.Frame(assist_frame)
        control_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(control_frame, text="Status:").pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_assist_status = ttk.Label(control_frame, text="Inactive", foreground="red")
        self.stop_assist_status.pack(side=tk.LEFT, padx=(0, 20))
        
        activate_assist_btn = ttk.Button(control_frame, text="Activate Stop Assist", 
                                         command=self.toggle_stop_assist, style='Activate.TButton')
        activate_assist_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        deactivate_assist_btn = ttk.Button(control_frame, text="Deactivate Stop Assist", 
                                           command=self.toggle_stop_assist, style='Deactivate.TButton')
        deactivate_assist_btn.pack(side=tk.LEFT)
        
    def create_motor_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Motor Controls")
        
        # Motor Testing Section
        motors_frame = ttk.LabelFrame(tab, text="Motor Testing", padding="10")
        motors_frame.pack( fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        #Create two columns for motors
        left_frame = ttk.Frame(motors_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        right_frame = ttk.Frame(motors_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Motor 1 Controls
        motor1_frame = ttk.LabelFrame(left_frame, text="Motor 1", padding="10")
        motor1_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(motor1_frame, text="Control Direction:", font=('Arial', 10, 'bold')).pack(pady=10)
        
        motor1_btn_frame = ttk.Frame(motor1_frame)
        motor1_btn_frame.pack(pady=10)
        
        ttk.Button(motor1_btn_frame, text="Turn Left", 
                  command=lambda: self.control_motor(1, "left")).pack(side=tk.LEFT, padx=5)
        ttk.Button(motor1_btn_frame, text="Stop", 
                  command=lambda: self.control_motor(1, "stop")).pack(side=tk.LEFT, padx=5)
        ttk.Button(motor1_btn_frame, text="Turn Right", 
                  command=lambda: self.control_motor(1, "right")).pack(side=tk.LEFT, padx=5)
        
        # Motor 2 Controls
        motor2_frame = ttk.LabelFrame(right_frame, text="Motor 2", padding="10")
        motor2_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(motor2_frame, text="Control Direction:", font=('Arial', 10, 'bold')).pack(pady=10)
        
        motor2_btn_frame = ttk.Frame(motor2_frame)
        motor2_btn_frame.pack(pady=10)
        
        ttk.Button(motor2_btn_frame, text="Turn Left", 
                  command=lambda: self.control_motor(2, "left")).pack(side=tk.LEFT, padx=5)
        ttk.Button(motor2_btn_frame, text="Stop", 
                  command=lambda: self.control_motor(2, "stop")).pack(side=tk.LEFT, padx=5)
        ttk.Button(motor2_btn_frame, text="Turn Right", 
                  command=lambda: self.control_motor(2, "right")).pack(side=tk.LEFT, padx=5)
    
    # Control Functions
    def toggle_lidar(self):
        self.lidar_active = not self.lidar_active
        if self.lidar_active:
            self.lidar_status.config(text="Active", foreground="green")
            self.update_status("LIDAR activated")
        else:
            self.lidar_status.config(text="Inactive", foreground="red")
            self.update_status("LIDAR deactivated")
    
    def toggle_camera(self):
        self.camera_active = not self.camera_active
        if self.camera_active:
            self.camera_status.config(text="Active", foreground="green")
            self.update_status("Camera activated")
        else:
            self.camera_status.config(text="Inactive", foreground="red")
            self.update_status("Camera deactivated")
    
    def toggle_stop_assist(self):
        self.stop_assist_active = not self.stop_assist_active
        if self.stop_assist_active:
            self.stop_assist_status.config(text="Active", foreground="green")
            self.update_status("Stop Assist activated")
        else:
            self.stop_assist_status.config(text="Inactive", foreground="red")
            self.update_status("Stop Assist deactivated")
    
    # def control_motor(self, motor_num, direction):
    #     self.update_status(f"Motor {motor_num} - {direction}")
    #     # Here you would add the actual code to control the motors
    
    def update_status(self, message):
        self.status_label.config(text=message)
        # Print to console for debugging
        print(message)

# Main application
if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(True, True)
    
    # Optional: Add app icon
    # root.iconbitmap('icon.ico')
    
    app = ControlPanel(root)
    root.mainloop()