import requests
import re
import tkinter as tk

def get_prompt():
    # Create the pop-up window
    window = tk.Tk()
    window.title("Enter prompt")
    
    # Set the window size and position
    window.geometry("400x200+{}+{}".format(
        int(window.winfo_screenwidth()/2 - 200),
        int(window.winfo_screenheight()/2 - 100)
    ))
    
    # Add a label and a text entry field
    tk.Label(window, text="Prompt:").pack()
    entry = tk.Entry(window)
    entry.pack()
    
    # Add a button to submit the prompt
    def submit():
        global prompt
        prompt = entry.get()
        window.destroy()
    
    tk.Button(window, text="Submit", command=submit).pack()
    
    # Run the pop-up window
    window.mainloop()

def shorten_url(long_url):
    # Set the API endpoint and the long URL to shorten
    api_endpoint = "https://tinyurl.com/api-create.php"
    params = {"url": long_url}
    
    # Send the request and get the response
    response = requests.get(api_endpoint, params=params)
    
    if response.status_code == 200:
        # If the request is successful, the response will contain the shortened URL
        return response.text
    else:
        # If the request is unsuccessful, the response will contain an error message
        return f"Error: {response.status_code} {response.reason}"

# Show the pop-up and get the prompt from the user
get_prompt()
print(f"Prompt: {prompt}")

# Set the API endpoint and your API key
api_endpoint = "https://api.openai.com/v1/images/generations"
api_key = "ENTER YOUR OWN KEY HERE"

# Set the request parameters
data = {
    "model": "image-alpha-001",
    "prompt": prompt,
    "num_images": 1,
    "size": "1024x1024",
    "response_format": "url"
}

# Send the request and get the response
response = requests.post(api_endpoint, json=data, headers={
    "Authorization": f"Bearer {api_key}"
})

if response.status_code == 200:
    # If the request is successful, the response will contain a URL to the generated image
    image_url = response.json()["data"][0]["url"]
    # Shorten a URL
    short_url = shorten_url(image_url)
    print(f"Short URL: {short_url}")
    
    # Use the requests library to download the image from the URL
    image_response = requests.get(image_url)
    if image_response.status_code == 200:
        # If the image request is successful, create a file name based on the prompt
        # Replace spaces and non-alphanumeric characters with underscores
        file_name = re.sub(r"[^\w\s]", "_", prompt)
        file_name = file_name.replace(" ", "_") + ".png"
        
        # Save the image data to the file
        with open(file_name, "wb") as f:
            f.write(image_response.content)
        print(f"Image saved to file: {file_name}")
    else:
        print(f"Error downloading image: {image_response.json()['message']}")
else:
    # If the request is unsuccessful, the response will contain an error message
    print(f"Error: {response.json()['message']}")