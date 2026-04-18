For each `.html` file in the current working directory, apply all of the following transformations:

1. **Add stylesheet link**: Insert `<link rel="stylesheet" href="../../../wtvstyles.css">` on the line immediately after `<head>`, unless it is already present.

2. **Add footer**: Insert the following block immediately before the closing `</body>` tag, unless a `<footer>` element is already present:
   ```
   <footerborder></footerborder>
   <footer>
     <div class=footerstatus>WebTV SpaceRace</div><div class=audiostatus><div class="audiogreen"></div>
     </div>
   </footer>
   ```

3. **Replace `absheight`**: Replace every occurrence of `absheight` (case-insensitive) with `height`.

4. **Replace `abswidth`**: Replace every occurrence of `abswidth` (case-insensitive) with `width`.

5. **Comment out and keep the Embed tags**: Comment out the embed tags, we will use those later.

6. **Adjust logo**: Position the logo in the webtv jewel cell td with align=center and valign=top.

7. **Replace file://**: Replace file:// with /.

8. **Adjust SCORE&NEXT ROW**: Wrap the Score, number digits and next arrow with a table like so:
```        <!-- //SCORE&NEXT ROW -->

        <tr>
          <td colspan=3>
            <!-- //SCORE CELL -->
            <table width=100%>
              <tr>
                <td valign=absmiddle align=center><font size=+2>Score:</font></td>

                <td valign=absmiddle>
                  <img width=33 height=53 src=/ROMCache/spacer.gif name=scorem>
                  <img width=33 height=53 src=/ROMCache/spacer.gif name=score0>
                  <img width=33 height=53 src=/ROMCache/spacer.gif name=score1>
                  <img width=33 height=53 src=/ROMCache/spacer.gif name=score2>
                  <img width=33 height=53 src=/ROMCache/spacer.gif name=score3>
                </td>

                <!-- // NEXT ARROW -->

                <td valign=absmiddle align=center>
                  <a href="javascript:RedirectToNextQuestion('general', 1)">
                    <img width=84 height=51 src="../../images/arrow.gif">
                  </a>
                </td>
              </tr>
            </table>
          </td>
          <!-- // SCORE&NEXT -->
   ``` and keep the src for the imgs as they are in the file.

9. **Re-indent**: Re-indent the entire file with consistent 2-space indentation. HTML structure rules:
   - `<html>`, `<!DOCTYPE>` at column 0
   - `<head>`, `<body>` indented 2 spaces
   - All children indented 2 spaces relative to their parent
   - Inline elements (e.g. `<a>`, `<span>`, `<b>`, `<i>`) may stay on the same line as their parent text
   - Script content indented 2 spaces inside `<script>` tags
   - Preserve blank lines that separate logical sections

Process every `.html` file in the current directory (not subdirectories). Read each file, apply all transformations, and write it back. After finishing all files, report which files were changed and what was done.
