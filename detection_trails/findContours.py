def find_contours(image):
    def dfs(row, col, contour):
        stack = [(row, col)]
        while stack:
            r, c = stack.pop()
            if 0 <= r < numrows and 0 <= c < numcols and image[r][c] == 1:
                contour.append([r, c])
                image[r][c] = 0  # Mark the current pixel as visited
                # Add unvisited neighbors to the stack
                stack.extend([(r + dr, c + dc) for dr in range(-1, 2) for dc in range(-1, 2)])
        return contour

    numrows = len(image)
    numcols = len(image[0])
    contours = []
    counters = []

    for i in range(numrows):
        for j in range(numcols):
            if image[i][j] == 1:
                contour = dfs(i, j, [])
                contours.append(contour)
                counters.append(len(contour))

    return contours, counters