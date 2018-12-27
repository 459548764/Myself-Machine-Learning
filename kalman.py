def kalman_init(data):
    data = np.array(data,dtype=float)
    err = []
    for i in range(1,data.shape[0]):
        err.append(abs(data[i] - data[i-1]))
    # figure out abs_err
    err = np.array(err,dtype=float)
    Q = np.mean(err)/data.shape[0]
    R = np.std(data)
    # Q often smaller than R
    return Q,R

def kalman_start(data,Q,R):
    data = np.array(data,dtype=float)
    result = []
    result.append(data[0])
    P = Q
    for i in range(1,data.shape[0]):
        Pk = P + Q
        K = Pk/(Pk+R)
        X = data[i-1] + K*(data[i] - data[i-1])
        P = (1-K)*Pk
        data[i] = X
        result.append(X)
    return result
