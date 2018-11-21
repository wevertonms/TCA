function quickSort(x, r, s)
    if (s <= r)
        return x
    end
    pivot = x[r]
    pivotID = r
    for i = (r + 1):s
        if (x[i] < pivot)
            aux = x[i]
            x[i] = x[pivotID + 1]
            x[pivotID + 1] = pivot
            x[pivotID] = aux
            pivotID = pivotID + 1
        end
    end
    quickSort(x, r, pivotID)
    quickSort(x, pivotID + 1, s)
    return x
end
quickSort!
sortperf(n) = quickSort!(rand(n), 1, n)
sortperf(10^4)
