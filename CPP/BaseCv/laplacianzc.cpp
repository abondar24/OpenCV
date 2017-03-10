#include "laplacianzc.h"

void LaplacianZC::setAperture(int a){
    aperture = a;
 }

cv::Mat  LaplacianZC::computeLaplacian(const cv::Mat& image){

    // compute Laplacian
    cv::Laplacian(image,laplace,CV_32F,aperture);

    // Keep local copy of the image for zero-crossings
    img = image.clone();

    return laplace;
}

// get the Laplacian result in 8-bit image
// zero = gray level 128
// if no scale provided - max scale will be scaled to intensity 255
cv::Mat  LaplacianZC::getLaplacianImage(double scale){
    if (scale<0){
        double lapmin, lapmax;

        cv::minMaxLoc(laplace, &lapmin, &lapmax);

        scale = 127/std::max(-lapmin, lapmax);
    }

    cv::Mat laplaceImage;
    laplace.convertTo(laplaceImage,CV_8U,scale,128);

    return laplaceImage;
}


 cv::Mat LaplacianZC::getZeroCrossings(float threshold){
     cv::Mat_<float>::const_iterator it =
             laplace.begin<float>() + laplace.step1();

     cv::Mat_<float>::const_iterator itend = laplace.end<float>();
     cv::Mat_<float>::const_iterator itup = laplace.begin<float>();

     // bin image init to white
     cv::Mat binary(laplace.size(),CV_8U,cv::Scalar(255));
     cv::Mat_<uchar>::iterator itout = binary.begin<uchar>() + binary.step1();

     // negate the input threshold value
     threshold *= -1.0;

     for (; it!= itend; ++it, ++itup, ++itout){
         // if the product of two adjascent pixel is
         // negative then there is a sign change
         if (*it * *(it-1) < threshold){
             // horizontal zero-crossing
             *itout = 0;
         } else if(*it * *itup < threshold){
             //vertical zero-crossing
             *itout = 0;
         }
     }

     return binary;
 }
