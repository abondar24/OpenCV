#ifndef COLORDETECOR_H
#define COLORDETECOR_H

#include <opencv2/core/core.hpp>

class ColorDetecor{
public:

    ColorDetecor(): minDist(100){
        target[0] = target[1] = target[2] = 0;
    }

    int getDistance(const cv::Vec3b& color) const;

    cv::Mat process(const cv::Mat &image);

    void setColorDistanceThreshold(int distance);

    int getColorDistanceThreshold();

    void setTargetColor(unsigned char red,
                        unsigned char green,
                        unsigned char blue);

    void setTargetColor(cv::Vec3b color);

    cv::Vec3b getTargetColor() const;

private:

    int minDist;
    cv::Vec3b target;
    cv::Mat result;
};

#endif // COLORDETECOR_H
