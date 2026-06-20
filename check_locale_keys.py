import yaml
import sys

def load_locale(path):
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def get_all_keys(data, prefix=''):
    keys = []
    if isinstance(data, dict):
        for k, v in data.items():
            new_prefix = f"{prefix}.{k}" if prefix else k
            if isinstance(v, dict):
                keys.extend(get_all_keys(v, new_prefix))
            elif isinstance(v, str):
                keys.append(new_prefix)
            # ignore non-string values like numbers
    return keys

def main():
    en_data = load_locale('./locales/en.yaml')
    zh_data = load_locale('./locales/zh-TW.yaml')
    
    en_keys = set(get_all_keys(en_data))
    zh_keys = set(get_all_keys(zh_data))
    
    # Keys we need from screener explanation
    needed_keys = {
        # from provider direct t() calls
        'screener.explanation.fallback',
        'screener.explanation.implication.dividend',
        'screener.explanation.implication.growth',
        'screener.explanation.implication.value',
        'screener.explanation.filter.revenue_positive',
        'screener.explanation.filter.industry_match',
        'screener.explanation.filter.per_range',
        'screener.explanation.filter.div_range',
        'screener.explanation.implication.custom_many',
        'screener.explanation.implication.custom_fallback',
        'screener.explanation.implication.default',
        'screener.explanation.filter.all_industries',
        # from screener_templates.yaml (template keys)
        'screener.explanation.preset.dividend.high_yield',
        'screener.explanation.preset.dividend.stable',
        'screener.explanation.preset.dividend.fallback',
        'screener.explanation.preset.dividend.implication',
        'screener.explanation.preset.growth.strong',
        'screener.explanation.preset.growth.moderate',
        'screener.explanation.preset.growth.fallback',
        'screener.explanation.preset.growth.implication',
        'screener.explanation.preset.value.deep_value',
        'screener.explanation.preset.value.moderate_value',
        'screener.explanation.preset.value.fallback',
        'screener.explanation.preset.value.implication',
        'screener.explanation.custom_filter.revenue_positive',
        'screener.explanation.custom_filter.industry_match',
        'screener.explanation.custom_filter.per_range',
        'screener.explanation.custom_filter.div_range',
        'screener.explanation.custom_filter.fallback',
        'screener.explanation.custom_filter.implication',
        'screener.explanation.disclaimer',
    }
    
    missing_in_en = needed_keys - en_keys
    missing_in_zh = needed_keys - zh_keys
    
    if missing_in_en:
        print("Missing keys in en.yaml:")
        for k in sorted(missing_in_en):
            print(f"  {k}")
    else:
        print("All needed keys present in en.yaml")
        
    if missing_in_zh:
        print("Missing keys in zh-TW.yaml:")
        for k in sorted(missing_in_zh):
            print(f"  {k}")
    else:
        print("All needed keys present in zh-TW.yaml")
        
    if not missing_in_en and not missing_in_zh:
        print("\nAll locale keys are present.")
        return 0
    else:
        return 1

if __name__ == '__main__':
    sys.exit(main())