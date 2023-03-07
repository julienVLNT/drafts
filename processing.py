import numpy as np

def autocorrelation(img: np.ndarray) -> np.ndarray:
    
    img_ = np.fft.fft2(img)
    img_ = np.power(np.abs(img_), 2)
    img_ = np.fft.ifft2(img_)
    img_ = np.abs(np.fft.fftshift(img_)/np.nanmax(img_))

    return img_



def cinf(img: np.ndarray) -> float:
    cinf_ = (1 +(np.power(img.mean(), 2) /np.power(autocorrelation(img), 2).mean())) /2.
    return cinf_



def length_vs_angle(auto: np.ndarray, cinf: float, angle: float) -> float:
    raise NotImplementedError
