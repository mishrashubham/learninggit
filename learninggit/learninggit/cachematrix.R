## Put comments here that give an overall description of what your
## functions do

## Write a short comment describing this function
## This program takes a matrix, calculates the inverse and caches it. Next time when the call comes to get the inverse of matrix,
## the cache is looked upon. If the inverse of that matrix is already cached, it is retrieved from cache instead of recalculating it 
## hence saving the computation time.

## makeCacheMatrix - This function caches the matrix and it's inverse. Functions get(),set(),getInverse(),setInverse() are defined in it to get the matrix,
## display the matrix, get the inverse of matrix and display the inverse of matrix respectively. 

makeCacheMatrix <- function(x = matrix()) {
  inv <- NULL
  set <- function(y) {
    x <<- y
    inv <<- NULL
  }
  get <- function() x
  setInverse <- function(inverse) inv <<- inverse
  getInverse <- function() inv
  list(set = set,
       get = get,
       setInverse = setInverse,
       getInverse = getInverse)
}


## cacheSolve - This matrix calculates the inverse of the matrix and caches the inverse.

cacheSolve <- function(x, ...) {
  ## Return a matrix that is the inverse of 'x'
  inv <- x$getInverse()
  if (!is.null(inv)) {
    message("getting cached data")
    return(inv)
  }
  mat <- x$get()
  inv <- solve(mat, ...)
  x$setInverse(inv)
  inv
}
