import pandas as pd
import requests
from io import StringIO
import os


def scrape_full_history():
    url = "https://www.esportstales.com/rocket-league/seasonal-rank-distribution-and-players-percentage-by-tier"
    headers = {"User-Agent": "Mozilla/5.0"}

    print("🚀 Ξεκινάει η πλήρης εξαγωγή (Season 20 -> Season 1)...")

    try:
        response = requests.get(url, headers=headers)
        tables = pd.read_html(StringIO(response.text))
        print(f"📊 Βρέθηκαν συνολικά {len(tables)} πίνακες.")

        all_data = []
        # Ξεκινάμε από την κορυφή (Season 20)
        current_season = 20

        # Θα διατρέξουμε τους πίνακες. Κάθε σεζόν έχει 2.
        # Χρησιμοποιούμε range μέχρι το τέλος των πινάκων
        for i in range(0, len(tables), 2):
            if current_season < 1: break

            print(f"--- Επεξεργασία Season {current_season} ---")

            # 1. Standard Modes Table
            try:
                df_std = tables[i].copy()
                df_std.rename(columns={df_std.columns[0]: 'Rank'}, inplace=True)
                df_melted_std = df_std.melt(id_vars=['Rank'], var_name='Mode', value_name='Percentage')
                df_melted_std['Category'] = 'Standard'
                df_melted_std['Season'] = current_season
                all_data.append(df_melted_std)
                print(f"   ✅ Standard OK")
            except Exception as e:
                print(f"   ⚠️ Σφάλμα στο Standard S{current_season}")

            # 2. Extra Modes Table
            try:
                # Επειδή η Season 1 έχει το "Summary" ενδιάμεσα,
                # αν δούμε ότι ο επόμενος πίνακας δεν είναι Extra, τον ψάχνουμε
                df_ext = tables[i + 1].copy()
                df_ext.rename(columns={df_ext.columns[0]: 'Rank'}, inplace=True)

                # Έλεγχος αν ο πίνακας είναι όντως Extra (συνήθως έχει στήλη Rumble)
                df_melted_ext = df_ext.melt(id_vars=['Rank'], var_name='Mode', value_name='Percentage')
                df_melted_ext['Category'] = 'Extra'
                df_melted_ext['Season'] = current_season
                all_data.append(df_melted_ext)
                print(f"   ✅ Extra OK")
            except Exception as e:
                print(f"   ⚠️ Σφάλμα στο Extra S{current_season}")

            current_season -= 1

        # Τελικό συμμάζεμα
        if all_data:
            final_df = pd.concat(all_data, ignore_index=True)

            # Καθαρισμός αριθμών
            final_df['Percentage'] = (
                final_df['Percentage']
                .astype(str)
                .str.replace('%', '', regex=False)
                .str.replace(',', '.', regex=False)
                .str.strip()
            )
            final_df['Percentage'] = pd.to_numeric(final_df['Percentage'], errors='coerce')
            final_df = final_df.dropna(subset=['Percentage'])

            if not os.path.exists('data'): os.makedirs('data')
            final_df.to_csv('data/seasonal_master.csv', index=False)

            print("\n" + "=" * 30)
            print(f"🏆 ΟΛΟΚΛΗΡΩΘΗΚΕ! Season 20 έως {current_season + 1}")
            print(f"📝 Συνολικές γραμμές: {len(final_df)}")
            print("=" * 30)

    except Exception as e:
        print(f"🚨 Κρίσιμο Σφάλμα: {e}")


if __name__ == "__main__":
    scrape_full_history()