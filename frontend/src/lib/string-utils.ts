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
    return s.split('_').map(capitalize).join('');
}

/**
 * Helper function that capitalizes the first letter of a string
 * @param s The string to capitalize
 * @returns The capitalized string
 */
export function capitalize(s: string): string {
    return s.charAt(0).toUpperCase() + s.slice(1);
}
