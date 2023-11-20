import subprocess

def burn_ventoy(image_path, target_device):
    try:
        # Run the dd command to burn the Ventoy image to the target device
        subprocess.run(['dd', 'if=' + image_path, 'of=' + target_device, 'bs=4M', 'status=progress'], check=True)
        print("Ventoy burned successfully!")
    except subprocess.CalledProcessError as e:
        print("Error burning Ventoy:", e)

# Specify the path to the Ventoy image file and the target device
image_path = '/path/to/ventoy.img'
target_device = '/dev/sdX'  # Replace 'sdX' with the appropriate device identifier

# Call the burn_ventoy function with the image path and target device
burn_ventoy(image_path, target_device)


