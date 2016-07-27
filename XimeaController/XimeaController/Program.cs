using System;
using System.Collections.Generic;
using System.Text;
using System.Collections;
using System.Drawing;
using System.Windows.Media.Imaging;
using System.IO;
using System.Threading;
using xiApi.NET;
using System.IO.Pipes;
using System.Drawing.Imaging;

namespace xiAPI.NET_example
{
    class Program
    {
        private static xiCam myCam;
        private static NamedPipeServerStream server;
        private static BinaryWriter pipeWriter;
        private static readonly string imagePath = "images";
        private static readonly string pipeName = "XimeaPipe";
        private static int exposure = 250;
        private static int numberOfImages = 3;
        private static float gain = 5;

        static void Main(string[] args)
        {
            try
            {
                formatPipe();
                try
                {
                    formatCamera();
                    //------------------------------------------------------------------------------------
                    // Capture images using safe buffer policy
                    Console.WriteLine("");
                    Console.WriteLine("Capturing images with safe buffer policy");
                    int width = 0, height = 0;
                    // image width must be divisible by 4
                    myCam.GetParam(PRM.WIDTH, out width);
                    myCam.SetParam(PRM.WIDTH, width - (width % 4));
                    myCam.GetParam(PRM.WIDTH, out width);
                    myCam.GetParam(PRM.HEIGHT, out height);
                    Bitmap safeImage = new Bitmap(width, height, System.Drawing.Imaging.PixelFormat.Format8bppIndexed);
                    myCam.SetParam(PRM.BUFFER_POLICY, BUFF_POLICY.SAFE);
                    //------------------------------------------------------------------------------------
                    // Start image acquisition
                    myCam.StartAcquisition();
                    //Bitmap myImage;
                    int timeout = 10000;

                    pipeWriter.Write((uint)numberOfImages);
                    for (int count = 0; count < numberOfImages; count++)
                    {
                        myCam.GetImage(safeImage, timeout);
                        //string fName = string.Format(imagePath + "/BWimage{0}.png", count);
                        byte[] imageBytes = Encoding.ASCII.GetBytes(imageToBase64(safeImage));
                        pipeWriter.Write((uint)imageBytes.Length);
                        pipeWriter.Write(imageBytes);
                        //Console.WriteLine("Got image: {0}, size {1}x{2} saving to {3}", count, safeImage.Width, safeImage.Height, fName);
                        //safeImage.Save(fName);
                    }

                    myCam.StopAcquisition();
                }
                catch (System.ApplicationException appExc)
                {
                    Console.WriteLine(appExc.Message);
                    Thread.Sleep(3000);
                    myCam.CloseDevice();
                }
            }
            catch (EndOfStreamException) { }
            Console.WriteLine("Client disconnected.");
            server.Close();
            server.Dispose();
        }

        static void formatCamera()
        {
            myCam = new xiCam();
            Directory.CreateDirectory(imagePath);
            int numDevices = 0;
            myCam.GetNumberDevices(out numDevices);
            if (0 == numDevices)
            {
                Console.WriteLine("No devices found");
                Thread.Sleep(3000);
                return;
            }
            else
            {
                Console.WriteLine("Found {0} connected devices.", numDevices);
            }
            // Initialize the device and return the device handle.
            myCam.OpenDevice(0);
            // Get device model name
            string strVal;
            myCam.GetParam(PRM.DEVICE_NAME, out strVal);
            Console.WriteLine("Found device {0}.", strVal);
            // Get device type
            myCam.GetParam(PRM.DEVICE_TYPE, out strVal);
            Console.WriteLine("Device type {0}.", strVal);
            // Get device serial number
            myCam.GetParam(PRM.DEVICE_SN, out strVal);
            Console.WriteLine("Device serial number {0}", strVal);
            myCam.SetParam(PRM.EXPOSURE, exposure);
            Console.WriteLine("Exposure was set to {0} microseconds", exposure);
            myCam.SetParam(PRM.GAIN, gain);
            Console.WriteLine("Gain was set to {0} decibels.", gain);

            // Set image output format to monochrome 8 bit
            myCam.SetParam(PRM.IMAGE_DATA_FORMAT, IMG_FORMAT.MONO8);
        }

        static void formatPipe()
        {
            // Open the named pipe.
            server = new NamedPipeServerStream(pipeName);
            Console.WriteLine("Waiting for connection...");
            server.WaitForConnection();
            Console.WriteLine("Connected.");
            pipeWriter = new BinaryWriter(server);
        }

        static string imageToBase64(Image image)
        {
            using (MemoryStream m = new MemoryStream())
            {
                Console.WriteLine(m.CanRead);
                image.Save(m, ImageFormat.Bmp);
                byte[] imageBytes = m.ToArray();

                // Convert byte[] to Base64 String
                string base64String = Convert.ToBase64String(imageBytes);
                return base64String;
            }
        }
    }
}
