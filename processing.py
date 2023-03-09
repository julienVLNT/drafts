import numpy as np

def autocorrelation(img: np.ndarray) -> np.ndarray:
    
    img_ = np.fft.fft2(img)
    img_ = np.power(np.abs(img_), 2)
    img_ = np.fft.ifft2(img_)
    img_ = np.abs(np.fft.fftshift(img_)/np.nanmax(img_))

    return img_



def cinf(img: np.ndarray) -> float:
    cinf_ = np.power(img.mean(), 2) /np.power(img, 2).mean()
    return cinf_



def length_vs_angle(auto: np.ndarray, cinf: float, angle: float) -> float:
    length = 0.0

    N = auto.shape[0]
    
    if angle < 0:
        raise NotImplementedError
    
    elif angle > np.pi:
        angle = angle - np.pi

    else:
        pass
    
    if angle < np.pi /2.:
        j_ = np.linspace(0, N/2-1, int(N/2)).astype(np.int32)
        i_ = np.round(j_ *np.tan(angle)).astype(np.int32)

        j_ = j_[i_ < N//2]
        i_ = i_[i_ < N//2]

        for i, j in zip(i_, j_):
            if auto[N//2-i, N//2+j] >= cinf:
                continue
            else:
                length = np.sqrt( (i)**2 + (j)**2 )
                break

    else:
        angle = np.pi - angle
        j_ = np.linspace(0, N/2-1, int(N/2)).astype(np.int32)
        i_ = np.round(j_ *np.tan(angle)).astype(np.int32)

        j_ = j_[i_ < N//2]
        i_ = i_[i_ < N//2]

        for i, j in zip(i_, j_):
            if auto[N//2-i, N//2-j] >= cinf:
                continue
            else:
                length = np.sqrt( (i)**2 + (j)**2 )
                break
    
    return length



def radial_profile(img: np.ndarray, angle: float) -> tuple:

    auto = autocorrelation(img)

    N  = img.shape[0]
    j_ = np.linspace(0, N//2-1, N//2).astype(np.int32)

    if angle < 0 or angle > 2*np.pi: raise NotImplementedError

    if angle > np.pi: angle = angle - np.pi

    if angle < np.pi /2.:
        i_ = np.round(j_ *np.tan(angle)).astype(np.int32)

        j_ = j_[i_ < N//2]
        i_ = i_[i_ < N//2]

        r      = np.zeros_like(j_)
        auto_r = np.zeros_like(j_)

        for k, (i, j) in enumerate(zip(i_, j_)):
            r[k]      = np.sqrt( np.power(j, 2) + np.power(i, 2) )
            auto_r[k] = auto[N//2-i, N//2+j]

    else:
        angle = np.pi - angle
        i_ = np.round(j_ *np.tan(angle)).astype(np.int32)

        j_ = j_[i_ < N//2]
        i_ = i_[i_ < N//2]

        r      = np.zeros_like(j_)
        auto_r = np.zeros_like(j_)

        for k, (i, j) in enumerate(zip(i_, j_)):
            r[k]      = np.sqrt( np.power(j, 2) + np.power(i, 2) )
            auto_r[k] = auto[N//2-i, N//2-j]

    return (r, auto_r)
