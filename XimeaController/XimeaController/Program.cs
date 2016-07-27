using System;
using System.Collections.Generic;
using System.Text;
using System.Collections;
using System.Drawing;
using xiApi.NET;

namespace XimeaController
{
    class Program
    {
        static void Main(string[] args)
        {
            xiCam myCam = new xiCam();

            try
            {
                // Initialize first camera
                myCam.OpenDevice(0);

                // Set device exposure to 2 milliseconds
                int exposure_us = 2000;
                myCam.SetParam(PRM.EXPOSURE, exposure_us);

                // Set device gain to 5 decibels
                float gain_db = 5;
                myCam.SetParam(PRM.GAIN, gain_db);

                // Set image output format to monochrome 8 bit
                myCam.SetParam(PRM.IMAGE_DATA_FORMAT, IMG_FORMAT.MONO8);

                // Capture images
                Bitmap myImage;
                int timeout = 1000;
                for (int i = 0; i < 10; i++)
                {
                    myCam.GetImage(out myImage, timeout);
                    string fName = string.Format("image{0}.bmp", i);
                    myImage.Save(fName);
                }
            }

            catch (System.ApplicationException appExc)
            {
                // Show handled error
                Console.WriteLine(appExc.Message);
                System.Console.ReadLine();
                myCam.CloseDevice();
            }

            finally
            {
                myCam.CloseDevice();
            }
        }
    }
    }
}
