using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Net.Sockets;
using System.Threading;
using System.Net;

namespace Visualization
{
    public partial class Form1 : Form
    {
        private TcpClient client;
        private NetworkStream stream;
        // Ball properties
        private int ballX = 100; // Initial X position
        private int ballY = 100; // Initial Y position
        private int ballRadius = 20; // Ball radius
        private int ballSpeed = 5; // Speed of ball movement
        int flag = 0;

        public Form1()
        {
            InitializeComponent();
        }

        private void Form1_Load(object sender, EventArgs e)
        {

            try
            {
                client = new TcpClient();
                client.Connect(IPAddress.Parse("172.20.10.12"), 5000); // Use the same IP and port as in the Python server code
                Console.WriteLine("Connected to the server.");

                stream = client.GetStream();

                // Start listening for data in a separate thread
                Thread receiveThread = new Thread(StartListeningForCoordinates);
                receiveThread.Start();

                Thread receiveThread2 = new Thread(StartListeningForData);
                receiveThread2.Start();

            }
            catch (Exception ex)
            {
                MessageBox.Show("Error: " + ex.Message);
            }

            
        }


        private void StartListeningForData()
        {
            byte[] buffer = new byte[1024];
            int bytesRead;

            while (true)
            {
                try
                {
                    bytesRead = stream.Read(buffer, 0, buffer.Length);
                    if (bytesRead > 0)
                    {
                        string data = Encoding.UTF8.GetString(buffer, 0, bytesRead);

                        if (data.StartsWith("TEXT:"))
                        {
                            string textData = data.Substring("TEXT:".Length);
                            DisplayReceivedText(textData);
                        }
                    }
                }
                catch (Exception ex)
                {
                    Console.WriteLine("Error: " + ex.Message);
                    break;
                }
            }
        }

        private void DisplayReceivedText(string textData)
        {
            if (!string.IsNullOrEmpty(textData))
            {
               //// Update textBox1 with the received text
               //textBox1.Invoke((Action)(() =>
               //{
               //    textBox1.AppendText(textData + Environment.NewLine);
               //}));
                
                if (textData.ToLower().Contains("light")&flag==0)
                {
                    flag = 1;
                    MessageBox.Show("Lights on");
                }
            }
        }
        private void StartListeningForCoordinates()
        {
            byte[] buffer = new byte[1024];
            int bytesRead;

            while (true)
            {
                try
                {
                    bytesRead = stream.Read(buffer, 0, buffer.Length);
                    if (bytesRead > 0)
                    {
                        string coordinates = Encoding.UTF8.GetString(buffer, 0, bytesRead);
                        DisplayCoordinates(coordinates);
                    }
                }
                catch (Exception e)
                {
                    Console.WriteLine("Error: " + e.Message);
                    break;
                }
            }

            // Clean up resources
            stream.Close();
            client.Close();
        }
        private void DisplayCoordinates(string coordinates)
        {
            if (coordinates != null)
            {
                // Split the received coordinates into left and right hand parts
                string[] handCoordinates = coordinates.Split('\n');

                if (handCoordinates.Length >= 1)
                {
                    string leftHandCoordinates = handCoordinates[0];
                    string[] leftHandParts = leftHandCoordinates.Split(',');

                    if (leftHandParts.Length >= 8) // Assuming the 4th point (thumb) is available
                    {
                        int thumbX = int.Parse(leftHandParts[6]); // Replace '6' with the correct index
                        int thumbY = int.Parse(leftHandParts[7]); // Replace '7' with the correct index

                        // Calculate new ball position based on thumb coordinates
                        ballX = thumbX;
                        ballY = thumbY;

                        // Redraw the ball
                        this.Invalidate();
                    }
                }
            }
        }

        protected override void OnPaint(PaintEventArgs e)
        {
            base.OnPaint(e);

            // Draw the ball at the new position
            e.Graphics.FillEllipse(Brushes.Red, ballX - ballRadius, ballY - ballRadius, 2 * ballRadius, 2 * ballRadius);

            // Get the position of the PictureBox
            Point pictureBoxLocation = pictureBox1.Location;
            int pictureBoxWidth = pictureBox1.Width;
            int pictureBoxHeight = pictureBox1.Height;

            // Check for collision between the ball and the PictureBox
            if (ballX >= pictureBoxLocation.X && ballX <= pictureBoxLocation.X + pictureBoxWidth &&
                ballY >= pictureBoxLocation.Y && ballY <= pictureBoxLocation.Y + pictureBoxHeight&&flag==1)
            {
                //Collision detected, trigger the "lights on" action
                flag = 0;
                MessageBox.Show("Lights on");
                
            }

            
        }

        private void pictureBox1_Click(object sender, EventArgs e)
        {

        }
    }
}