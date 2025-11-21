// snapService.js
const SNAP_THRESHOLD = 5

export const snapToElements = (movingElement, otherElements, dx, dy) => {
  const centerX = movingElement.x + dx + movingElement.width / 2
  const centerY = movingElement.y + dy + movingElement.height / 2

  let snappedX = movingElement.x + dx
  let snappedY = movingElement.y + dy

  otherElements.forEach((element) => {
    if (element.id === movingElement.id) return

    const elementCenterX = element.x + element.width / 2
    const elementCenterY = element.y + element.height / 2

    // Snap to center points
    if (Math.abs(centerX - elementCenterX) < SNAP_THRESHOLD) {
      snappedX = elementCenterX - movingElement.width / 2
    }

    if (Math.abs(centerY - elementCenterY) < SNAP_THRESHOLD) {
      snappedY = elementCenterY - movingElement.height / 2
    }
  })

  return { x: snappedX, y: snappedY }
}
