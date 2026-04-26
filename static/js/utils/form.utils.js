export class FormUtils {
    static extractFormData(formElem) {
        return $(formElem).serializeArray()
            .reduce((values, x) => {
                values[x.name] = x.value;
                return values;
            }, {});
    }
}