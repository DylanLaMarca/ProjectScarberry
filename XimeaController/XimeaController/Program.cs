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
        private static readonly string IMAGE_PATH = "images";
        private static readonly string PIPE_NAME = "XimeaPipe";
        private static readonly int PAUSE_TIME = 3000;

        private static ManualResetEvent sendPauseEvent = new ManualResetEvent(false);
        private static Bitmap[] images;
        private static bool formatCameraComplete = false;
        private static bool formatPipeComplete = false;
        private static bool formatImageListComplete = false;
        private static bool run = true;
        private static int approximatePicCount;
        private static int exposure;
        private static int timeout;
        private static float gain;
        private static int imageCount;

        private static NamedPipeServerStream server;
        private static BinaryWriter pipeWriter;
        private static BinaryReader pipeReader;
        private static Thread captureThread;
        private static Thread sendThread;
        private static xiCam myCam;

        static void Main(string[] args)
        {
            captureThread = new Thread(new ThreadStart(cameraThread));
            sendThread = new Thread(new ThreadStart(pipeThread));
            captureThread.Start();
            sendThread.Start();
        }

        static void cameraThread()
        {
            try
            {
                try
                {
                    formatCamera();
                    formatCameraComplete = true;
                    while (!formatImageListComplete) { }
                    myCam.SetParam(PRM.BUFFER_POLICY, BUFF_POLICY.SAFE);
                    myCam.StartAcquisition();
                    imageCount = 0;
                    while (run)
                    {
                        Console.WriteLine("Capturing image {0} with safe buffer policy", imageCount);
                        myCam.GetImage(images[imageCount], timeout);
                        sendPauseEvent.Set();
                        imageCount++;
                    }
                }
                catch (ApplicationException appExc)
                {
                    int counterValue;
                    myCam.GetParam(PRM.COUNTER_VALUE, out counterValue);
                    Console.WriteLine("Skipped Frames: {0}", counterValue);
                    myCam.StopAcquisition();
                    Console.WriteLine("AppErr: {0}", appExc.Message);
                    myCam.CloseDevice();
                }
            }
            catch (ThreadAbortException threadExc)
            {
                int counterValue;
                myCam.GetParam(PRM.COUNTER_VALUE, out counterValue);
                Console.WriteLine("Skipped Frames: {0}", counterValue);
                myCam.StopAcquisition();
                Console.WriteLine("ThreadErr: {0}", threadExc.Message);
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

            while (!formatPipeComplete) { }

            myCam.SetParam(PRM.EXPOSURE, exposure);
            Console.WriteLine("Exposure was set to {0} microseconds", exposure);
            myCam.SetParam(PRM.GAIN, gain);
            Console.WriteLine("Gain was set to {0} decibels.", gain);

            myCam.SetParam(PRM.TRG_SOURCE, TRG_SOURCE.EDGE_RISING);

            Console.WriteLine("Setting GPI Mode trigger.");
            myCam.SetParam(PRM.GPI_SELECTOR, 1);
            myCam.SetParam(PRM.GPI_MODE, GPI_MODE.TRIGGER);

            Console.WriteLine("Setting GPO Mode to active exposure.");
            myCam.SetParam(PRM.GPO_SELECTOR, 1);
            myCam.SetParam(PRM.GPO_MODE, GPO_MODE.EXPOSURE_ACTIVE);
            
            myCam.SetParam(PRM.IMAGE_DATA_FORMAT, IMG_FORMAT.MONO8);

            int maxBandwidth;
            myCam.GetParam(PRM.AVAILABLE_BANDWIDTH_MAX, out maxBandwidth);
            Console.WriteLine("Max Framerate: {0}", maxBandwidth);

            myCam.SetParam(PRM.AUTO_BANDWIDTH_CALCULATION, 0);

            int automaticBusSpeed;
            myCam.GetParam(PRM.AUTO_BANDWIDTH_CALCULATION, out automaticBusSpeed);
            Console.WriteLine("Bus Speed: {0}", automaticBusSpeed);

            myCam.SetParam(PRM.COUNTER_SELECTOR, COUNTER_SELECTOR.CNT_SEL_API_SKIPPED_FRAMES);
        }

        static void pipeThread()
        {
            try
            {
                try
                {
                    formatPipe();
                    timeout = 20000;
                    formatPipeComplete = true;
                    while (!formatCameraComplete) { }
                    formatImageList();
                    formatImageListComplete = true;
                    int count = 0;
                    while (run)
                    {
                        while (count < imageCount)
                        {
                            byte[] imageBytes = formatStringToPipe(images[count]);
                            Console.WriteLine("=========={0}", imageBytes.Length);
                            pipeWriter.Write((uint)imageBytes.Length);
                            pipeWriter.Write(imageBytes);
                            count++;
                        }
                        Console.WriteLine("sendThread: Wait");
                        sendPauseEvent.WaitOne();
                        sendPauseEvent.Reset();
                        Console.WriteLine("sendThread: Released");
                    }
                }
                catch (EndOfStreamException) { }
                Console.WriteLine("Client disconnected.");
                server.Close();
                server.Dispose();
                captureThread.Abort();
            }
            catch (ThreadAbortException threadExc)
            {
                Console.WriteLine("ThreadAbortException: {0}", threadExc.Message);
            }
        }

        static void formatPipe()
        {
            server = new NamedPipeServerStream(PIPE_NAME);
            Console.WriteLine("Waiting for client connection...");
            server.WaitForConnection();
            Console.WriteLine("Client connected.");
            pipeWriter = new BinaryWriter(server);
            pipeReader = new BinaryReader(server);
            exposure = (int)pipeReader.ReadUInt32();
            gain = (int)pipeReader.ReadUInt32();
            approximatePicCount = (int)pipeReader.ReadUInt32();
        }

        static void formatImageList()
        {
            Console.WriteLine("ImageList Length: {0}", approximatePicCount);
            images = new Bitmap[approximatePicCount];
            int width = 0, height = 0;
            // image width must be divisible by 4
            myCam.GetParam(PRM.WIDTH, out width);
            myCam.SetParam(PRM.WIDTH, (width - (width % 4))/4);
            myCam.GetParam(PRM.WIDTH, out width);
            myCam.GetParam(PRM.HEIGHT, out height);
            myCam.SetParam(PRM.HEIGHT, (height - (height % 4))/4);
            myCam.GetParam(PRM.HEIGHT, out height);
            Console.Write("ImageList adding SafeBitmap ");
            for (int count = 0; count < approximatePicCount; count++)
            {
                Console.Write("{0},",count);
                images[count] = new Bitmap(width, height, System.Drawing.Imaging.PixelFormat.Format8bppIndexed);
                if(count % 10 == 0)
                {
                    Console.WriteLine();
                }
            }
            Console.WriteLine();
        }

        static byte[] formatStringToPipe(Image image)
        {
            using (MemoryStream m = new MemoryStream())
            {
                image.Save(m, ImageFormat.Bmp);
                byte[] imageBytes = m.ToArray();
                string base64String = Convert.ToBase64String(imageBytes);
                return Encoding.ASCII.GetBytes(base64String);
            }
        }
    }
}