using System;
using System.Text;
using System.Drawing;
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
        private static readonly int pauseTime = 3000;
        private static int exposure = 250;
        private static int numberOfImages = 10;
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
                    Bitmap safeImage = createSafeBitmap();
                    myCam.SetParam(PRM.BUFFER_POLICY, BUFF_POLICY.SAFE);
                    myCam.StartAcquisition();
                    //for (int count = 0; count < numberOfImages; count++)
                    //{
                        myCam.GetImage(safeImage, 10000);
                        //byte[] imageBytes = formatStringToPipe(safeImage);
                        //pipeWriter.Write((uint)imageBytes.Length);
                        //pipeWriter.Write(imageBytes);
                        safeImage.Save("image.jpg");
                    //}

                    myCam.StopAcquisition();
                }
                catch (System.ApplicationException appExc)
                {
                    Console.WriteLine(appExc.Message);
                    Thread.Sleep(pauseTime);
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
                Thread.Sleep(pauseTime);
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

            myCam.SetParam(PRM.TRG_SOURCE, TRG_SOURCE.EDGE_RISING);

            Console.WriteLine("Setting GPI Mode trigger.");
            myCam.SetParam(PRM.GPI_SELECTOR, 1);
            myCam.SetParam(PRM.GPI_MODE, GPI_MODE.TRIGGER);

            Console.WriteLine("Setting GPO Mode to output exposure.");
            myCam.SetParam(PRM.GPO_SELECTOR, 1);
            myCam.SetParam(PRM.GPO_MODE, GPO_MODE.EXPOSURE_ACTIVE);

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

        static Bitmap createSafeBitmap()
        {
            int width = 0, height = 0;
            // image width must be divisible by 4
            myCam.GetParam(PRM.WIDTH, out width);
            myCam.SetParam(PRM.WIDTH, width - (width % 4));
            myCam.GetParam(PRM.WIDTH, out width);
            myCam.GetParam(PRM.HEIGHT, out height);
            return new Bitmap(width, height, System.Drawing.Imaging.PixelFormat.Format8bppIndexed);
        }

        static byte[] formatStringToPipe(Image image)
        {
            using (MemoryStream m = new MemoryStream())
            {
                Console.WriteLine(m.CanRead);
                image.Save(m, ImageFormat.Bmp);
                byte[] imageBytes = m.ToArray();
                string base64String = Convert.ToBase64String(imageBytes);
                return Encoding.ASCII.GetBytes(base64String);
            }
        }
    }
}
