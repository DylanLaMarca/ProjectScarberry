using System;
using System.Text;
using System.Drawing;
using System.IO;
using System.Threading;
using xiApi.NET;
using System.IO.Pipes;
using System.Drawing.Imaging;
using System.Collections.Generic;

namespace xiAPI.NET_example
{
    class Program
    {
        private static readonly string IMAGE_PATH = "images";
        private static readonly string PIPE_NAME = "XimeaPipe";
        private static readonly int PAUSE_TIME = 3000;

        private static ManualResetEvent sendPauseEvent = new ManualResetEvent(false);
        private static Queue<Bitmap> images = new Queue<Bitmap>();
        private static bool formatCameraComplete = false;
        private static bool formatPipeComplete = false;
        private static bool run = true;
        private static int exposure = 250;
        private static float gain = 5;

        private static NamedPipeServerStream server;
        private static BinaryWriter pipeWriter;
        private static Thread captureThread;
        private static Thread sendThread;
        private static xiCam myCam;

        static void Main(string[] args)
        {
            captureThread = new Thread(new ThreadStart(cameraThread));
            //sendThread = new Thread(new ThreadStart(pipeThread));
            captureThread.Start();
            //sendThread.Start();
        }

        static void cameraThread()
        {
            try
            {
                try
                {
                    formatCamera();
                    formatCameraComplete = true;
                    while (!formatCameraComplete && !formatPipeComplete) { }
                    Console.WriteLine("");
                    Bitmap safeImage = createSafeBitmap();
                    myCam.SetParam(PRM.BUFFER_POLICY, BUFF_POLICY.SAFE);
                    myCam.StartAcquisition();
                    int count = 0;
                    while (run)
                    {
                        Console.WriteLine("Capturing images with safe buffer policy");
                        myCam.GetImage(safeImage, 10000);
                        //images.Enqueue(safeImage);
                        //sendPauseEvent.Set();
                        String fileName = String.Format("images\\image{0}.png", count);
                        safeImage.Save(fileName);
                        count++;
                    }
                    myCam.StopAcquisition();
                }
                catch (ApplicationException appExc)
                {
                    Console.WriteLine("AppErr");
                    Console.WriteLine(appExc.Message);
                    myCam.CloseDevice();
                }
            }
            catch (ThreadAbortException threadExc)
            {
                Console.WriteLine("ThreadErr");
                Console.WriteLine(threadExc.Message);
                myCam.CloseDevice();
            }

            run = false;
            sendPauseEvent.Set();
            Thread.Sleep(250);
        }

        static void formatCamera()
        {
            myCam = new xiCam();
            Directory.CreateDirectory(IMAGE_PATH);
            int numDevices = 0;
            myCam.GetNumberDevices(out numDevices);
            if (0 == numDevices)
            {
                Console.WriteLine("No devices found");
                Thread.Sleep(PAUSE_TIME);
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

        static void pipeThread()
        {

            /*try
            {*/
            //formatPipe();
            formatPipeComplete = true;
            while (!formatCameraComplete && !formatPipeComplete) { }
            int count = 0;
            while (run)
            {
                while (images.Count > 0)
                {
                    Console.WriteLine(images.Count);
                    images.Dequeue().Save(string.Format("images\\image{0}.jpg", count));
                    count++;
                    /*byte[] imageBytes = formatStringToPipe(images.Dequeue());
                    pipeWriter.Write((uint)imageBytes.Length);
                    pipeWriter.Write(imageBytes);*/
                }
                Console.WriteLine("sendThread: Wait");
                sendPauseEvent.WaitOne();
                sendPauseEvent.Reset();
                Console.WriteLine("sendThread: Release");
            }
            /*}
            catch (EndOfStreamException) { 
                captureThread.Abort();
            }*/


            /*Console.WriteLine("Client disconnected.");
            server.Close();
            server.Dispose();
            captureThread.Abort();*/
        }

        static void formatPipe()
        {
            // Open the named pipe.
            server = new NamedPipeServerStream(PIPE_NAME);
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