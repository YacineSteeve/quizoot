/**
 * Helper function that converts from PascalCase to snake_case
 * @param s The string to convert
 * @returns The converted string
 */
export function pascalToSnake(s: string) {
    const pattern = /\.?([A-Z]+[a-z]*)/g;
    return s.replace(pattern, function (substring, ...args) {
        substring = substring.toLowerCase();
        if (args[1] > 0) {
            substring = '_' + substring;
        }
        return substring;
    });
}

/**
 * Helper function that converts from snake_case to PascalCase
 * @param s The string to convert
 * @returns The converted string
 */
export function snakeToPascal(s: string): string {
    return s
        .split('_')
        .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
        .join('');
}
